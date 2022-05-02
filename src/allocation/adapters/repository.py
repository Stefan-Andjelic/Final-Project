import abc
from allocation.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch, collection):
        self.session.add(batch)
        self.session.add(collection)

    def get_batch(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def get_item(self, reference):
        return self.session.query(model.Item).filter_by(reference=reference).one()

    def list_batch(self):
        return self.session.query(model.Batch).all()