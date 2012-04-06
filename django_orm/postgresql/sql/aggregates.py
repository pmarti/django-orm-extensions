# -*- coding: utf-8 -*-

from django.db.models.sql import aggregates
from django.db import models

class Unaccent(aggregates.Aggregate):
    sql_function = 'unaccent'

    def __init__(self, col, source=None, is_summary=False, **extra):
        source = models.CharField(max_length=10000)
        super(Unaccent, self).__init__(col, source, is_summary, **extra)


class ArrayLength(aggregates.Aggregate):
    sql_function = 'array_length'
    sql_template = '%(function)s(%(field)s, 1)'
    is_computed = True

    def __init__(self, col, source=None, is_summary=False, **extra):
        _sum = extra.pop('sum', False)
        if _sum:
            self.sql_template = "sum(%s)" % self.sql_template
        super(ArrayLength, self).__init__(col, source, is_summary=True, **extra)
