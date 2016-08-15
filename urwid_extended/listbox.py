#!/usr/bin/env python

import warnings

import urwid

__all__ = [
    'SortedFocusListWalker',
]

class SortedFocusListWalker(urwid.SimpleFocusListWalker):
    """
    This class triggers all operations of list manipulation to maintain the
    list sorted
    """
    def __init__(self, contents, sorting_key=lambda x: x, reverse=False):
        """
        :param contents: the contents to display (may be unsorted)
        :type contents: list

        :param sorting_key: function returning the value to compare between
            each item of the contents
        :type sorting_key: function

        :param reverse: indicate to reverse the sorted order or not
        :type reverse: bool

        >>> sw = SortedFocusListWalker([1,4,2,7,3]); sw
        SortedFocusListWalker([1, 2, 3, 4, 7], focus=0)
        >>> sw.add(5); sw
        SortedFocusListWalker([1, 2, 3, 4, 5, 7], focus=0)
        >>> len(sw)
        6
        >>> sw += [11, 0, 6]; sw
        SortedFocusListWalker([0, 1, 2, 3, 4, 5, 6, 7, 11], focus=1)
        >>> sw = SortedFocusListWalker([1,4,7,3], reverse=True); sw
        SortedFocusListWalker([7, 4, 3, 1], focus=0)
        >>> contents = [(1, 10), (4, 6), (0, 7)]
        >>> sw = SortedFocusListWalker(contents, sorting_key=lambda x: x[0])
        >>> sw
        SortedFocusListWalker([(0, 7), (1, 10), (4, 6)], focus=0)
        >>> sw = SortedFocusListWalker(contents, sorting_key=lambda x: x[1])
        >>> sw
        SortedFocusListWalker([(4, 6), (0, 7), (1, 10)], focus=0)
        """

        super().__init__(sorted(contents, key=sorting_key, reverse=reverse))
        self.sorting_key = sorting_key
        self.reverse = reverse

    def __setitem__(self, i, y):
        if isinstance(i, slice):
            raise NotImplementedError('__imul__ not usable for search')
        del self[i]
        return self.add(y)

    def __imul__(self, n):
        raise NotImplementedError('__imul__ not usable for search')

    def __iadd__(self, new_item):
        if isinstance(new_item, list):
            self.extend(new_item)
        else:
            self.add(new_item)
        return self

    def add(self, new_item):
        """
        Add the new_item in the list at the adequate position

        :param new_item: the inserted item

        >>> sw = SortedFocusListWalker([1,10]); sw
        SortedFocusListWalker([1, 10], focus=0)
        >>> sw.add(5); sw
        SortedFocusListWalker([1, 5, 10], focus=0)
        >>> sw.add(7); sw
        SortedFocusListWalker([1, 5, 7, 10], focus=0)
        >>> contents = [(1, 10), (4, 2), (0, 7)]
        >>> sw = SortedFocusListWalker(contents, sorting_key=lambda x: x[1], reverse=True)
        >>> sw.add((100, 4)); sw
        SortedFocusListWalker([(1, 10), (0, 7), (100, 4), (4, 2)], focus=0)
        """
        new_value = self.sorting_key(new_item)
        for index, item in enumerate(self):
            if (self.sorting_key(item) > new_value) ^ self.reverse:
                return super().insert(index, new_item)
        return super().append(new_item)

    def append(self, new_item):
        """
        .. warning:: This method is should not be use with
            SortedFocusListWalker class because the appended item is not
            garanted to be at the end of the sorted list

        See also :meth:`.add`
        """
        warnings.warn('Usage of SortedFocusListWalker.append is wrong. SortedFocusListWalker manage indexing itself. Use SortedFocusListWalker.add instead')
        return self.add(new_item)

    def extend(self, new_items):
        """
        Extend the sorted list with multiple, new_item

        :param new_items: the list of new item
        :type new_items: list

        >>> sw = SortedFocusListWalker([1,10]); sw
        SortedFocusListWalker([1, 10], focus=0)
        >>> sw.extend([0, 2, -10, 14]); sw
        SortedFocusListWalker([-10, 0, 1, 2, 10, 14], focus=2)
        >>> contents = [(1, 10), (4, 2), (0, 7)]
        >>> sw = SortedFocusListWalker(contents, sorting_key=lambda x: x[1], reverse=True)
        >>> sw.extend([(100, 4), (20, 20)]); sw
        SortedFocusListWalker([(20, 20), (1, 10), (0, 7), (100, 4), (4, 2)], focus=1)
        """
        for item in sorted(new_items, key=self.sorting_key, reverse=self.reverse):
            self.add(item)

    def insert(self, index, item):
        """
        .. warning:: This method is should not be use with
            SortedFocusListWalker class because the inserted item is not
            garanted to be at the index position in the sorted list

        See also :meth:`.add`
        """
        warnings.warn('Usage of SortedFocusListWalker.insert is wrong. SortedFocusListWalker manage indexing itself. Use SortedFocusListWalker.add instead')
        return self.add(item)

    def sort(self, sorting_key=lambda x: x, reverse=False):
        """
        Define the new sorting parameter for the list

        See also :meth:`.__init__`

        :param sorting_key: see :meth:`.__init__`

        :param reverse: see :meth:`.__init__`

        >>> contents = [(-1, 10), (30, -5), (4, 20), (0, 7)]
        >>> sw = SortedFocusListWalker(contents); sw
        SortedFocusListWalker([(-1, 10), (0, 7), (4, 20), (30, -5)], focus=0)
        >>> sw.sort(lambda x: x[1]); sw
        SortedFocusListWalker([(30, -5), (0, 7), (-1, 10), (4, 20)], focus=2)
        >>> sw.sort(reverse=True); sw
        SortedFocusListWalker([(30, -5), (4, 20), (0, 7), (-1, 10)], focus=3)
        >>> sw.add((2, 2)); sw
        SortedFocusListWalker([(30, -5), (4, 20), (2, 2), (0, 7), (-1, 10)], focus=4)
        """
        self.sorting_key = sorting_key
        self.reverse = reverse
        return super().sort(key=self.sorting_key, reverse=self.reverse)
        


def _test():
    import doctest
    doctest.testmod()

if __name__=='__main__':
    _test()

