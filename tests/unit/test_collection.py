
from allocation.domain.model import Collection, Item, Designer


def test_collection_has_sufficient_items():
    designer = Designer("Louis", "Gueye", 22, ['Louis x Stickman'])
    collection = Collection("Louis x Stickman", ["Black hoodie", "grey", "blue"], designer)

    assert collection.check_collection_quantity()


def test_collection_has_insufficient_items():
    designer = Designer("Louis", "Gueye", 22, ['Louis x Stickman'])
    collection = Collection("Louis x Stickman", ["Black hoodie"], designer)

    assert collection.check_collection_quantity() is False


def test_collection_has_designer():
    designer = Designer("Louis", "Gueye", 22, ['Louis x Stickman'])
    collection = Collection("Louis x Stickman", ["Black hoodie"], designer)

    assert collection.check_designer()


def test_collection_has_no_designer():
    collection = Collection("Louis x Stickman", ["Black hoodie"])

    assert collection.check_designer() is False


def test_designer_has_collection():
    designer = Designer("Louis", "Gueye", 22, ['Louis x Stickman', 'Louis x RED'])

    assert designer.has_collection()


def test_designer_has_no_collection():
    designer = Designer("Louis", "Gueye", 22, [])

    assert designer.has_collection() is False


def test_designer_is_old_enough():
    designer = Designer("Louis", "Gueye", 22, ['Louis x Stickman', 'Louis x RED'])

    assert designer.eligible_age()


def test_designer_is_not_old_enough():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])

    assert designer.eligible_age() is False


def test_item_has_designer():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])
    item = Item("Black Hoodie", 1, 99, designer)

    assert item.has_designer()


def test_item_has_no_designer():
    item = Item("Black Hoodie", 1, 99)

    assert item.has_designer() is False


def test_item_is_available():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])
    item = Item("Black Hoodie", 1, 99, designer)

    assert item.available_quantity()


def test_item_is_not_available():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])
    collection = Collection("Louis x Stickman", ["Black hoodie"], designer)
    item = Item("Black Hoodie", 0, 99, designer, collection)

    assert item.available_quantity() is False


def test_item_is_part_of_collection():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])
    collection = Collection("Louis x Stickman", ["Black hoodie"], designer)
    item = Item("Black Hoodie", 0, 99, designer, collection)

    assert item.in_collection()


def test_item_is_not_part_of_collection():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])
    item = Item("Black Hoodie", 0, 99, designer)

    assert item.in_collection() is False


# Does this one make sense
def test_item_is_in_too_many_collections():
    designer = Designer("Louis", "Gueye", 14, ['Louis x Stickman', 'Louis x RED'])
    collection1 = Collection("Louis x Stickman", ["Black hoodie"], designer)
    collection2 = Collection("Louis x RED", ["Red hoodie"], designer)
    collections = [collection1, collection2]
    item = Item("Black Hoodie", 0, 99, designer, collections)

    assert item.in_collection() is False


