from decimal import Decimal
from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import mapper, relationship

from allocation.domain import model


metadata = MetaData()

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("price", Float),
    Column("eta", Date, nullable=True),
    Column("designer_id", ForeignKey("designers.id")),
)

designers = Table(
    "designers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("firstName", String(255)),
    Column("lastName", String(255)),
    Column("age", Integer),
)

collections = Table(
    "collections",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(150)),
    Column("qty", Integer, nullable=False),
    Column("item_id", ForeignKey("items.id")),
    Column("designer_id", ForeignKey("designers.id")),
)

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    items_mapper = mapper(model.Item, items)
    designer_mapper = mapper(model.Designer, designers)
    lines_mapper = mapper(model.OrderLine, order_lines)
    mapper(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper(
        model.Collection,
        collections,
        properties={
            "_allocations": relationship(
                items_mapper,
                secondary=allocations,
                collection_class=set,
            )
        }
    )