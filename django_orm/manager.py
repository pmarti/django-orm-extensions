# -*- coding: utf-8 -*-

from django.db import models
from django.db import connections

class BaseManager(models.Manager):
    use_for_related_fields = True


class Manager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        connection = connections[self.db]
        if connection.vendor == 'postgresql':
            from django_orm.postgresql.query import PgQuerySet
            return PgQuerySet(model=self.model, using=self._db)
        elif connection.vendor == 'mysql':
            from django_orm.mysql.query import MyQuerySet
            return MyQuerySet(model=self.model, using=self._db)
        elif connection.vendor == 'sqlite':
            from django_orm.sqlite3.query import SqliteQuerySet
            return SqliteQuerySet(model=self.model, using=self._db)
        else:
            return super(Manager, self).get_query_set()

    def cache(self, *args, **kwargs):
        return self.get_query_set().cache(*args, **kwargs)

    def array_slice(self, attr, x, y, **params):
        """ Get subarray from some array field. Only for postgresql vendor. """
        return self.filter(**params).array_slice(attr, x, y)

    def array_length(self, attr, **params):
        """Get length from some array field. Only for postgresql vendor. """
        return self.filter(**params).array_length(attr)
