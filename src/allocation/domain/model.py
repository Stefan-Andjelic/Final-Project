from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set
from unicodedata import decimal


class OutOfStock(Exception):
    pass


# def allocate(line: OrderLine, batches: List[Batch]) -> str:
#     try:
#         batch = next(b for b in sorted(batches) if b.can_allocate(line))
#         batch.allocate(line)
#         return batch.reference
#     except StopIteration:
#         raise OutOfStock(f"Out of stock for sku {line.sku}")


@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

class Item:
    def __init__(self, sku: str, designer: Designer, collection: Collection, eta: Optional[date]):
        self.sku = sku
        self.designer = designer
        self.collection = collection
        self.eta = eta

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            # self.version_number += 1
            return batch.reference
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {line.sku}")

class Designer:
    def __init__(self, firstName: str, lastName: str, age: int, collections: List[Collection]):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self._collections = collections

    def has_collection(self) -> bool:
        return self._collections.__len__ > 0

    def eligible_age(self) -> bool:
        return self.age >= 18

    def add_collection(self, collection: Collection):
        return self._collections.add(collection)

    def has_designer(self):
        return self.designer

    def available_quantity(self) -> bool:
        return self.qty >= 1

    def in_collection(self) -> bool:
        return self.collection is True


class Collection:
    def __init__(self, name: str, items: List[Item], designer: Designer):
        # self.reference = ref
        self.name = name
        self.items = items
        self.designer = designer
        self._allocations = set()  # type: Set[Item]

    def check_collection_quantity(self) -> bool:
        return self.items.__len__ >= 3 and self.items.__len__ <= 10

    def check_designer(self) -> bool:
        return self.designer


