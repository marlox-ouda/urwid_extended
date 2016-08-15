#!/usr/bin/env python

import urwid
from urwid.container import WidgetContainerListContentsMixin

__all__ = [
    'SearchableWidgetWrapper',
]

class SearchableWidgetWrapper(urwid.WidgetWrap):
    """
    This class wrap a container and allow to focus on the looked field.
    The looked field is the first field that match the pressed key of
        the user
    """
    def __init__(self, wrapped_widget, looked_field=lambda x: x):
        """
        :param wrapped_widget: the container where the value will
            be look for
        :type wrapped_widget: ContainerListContentsMixin

        :param looked_field: function returning the lookable value
            for each item available in the wrapped_widget
        :type looked_field: function

        >>> items = ['abc','aab','aaa','bcd','bdd']
        >>> w = urwid.Pile(list(map(urwid.Text, items)))
        >>> sw = SearchableWidgetWrapper(w, lambda x: x.text)
        >>> sw.get_focus().text
        'abc'
        >>> silent=sw.keypress((40, 40), 'b'); sw.get_focus().text
        'bcd'
        >>> silent=sw.keypress((40, 40), 'b'); sw.get_focus().text
        'bcd'
        >>> silent=sw.keypress((40, 40), 'escape'); sw.get_focus().text
        'bcd'
        >>> silent=sw.keypress((40, 40), 'a'); sw.get_focus().text
        'abc'
        >>> silent=sw.keypress((40, 40), 'a'); sw.get_focus().text
        'aab'
        """
        super().__init__(wrapped_widget)
        if not isinstance(wrapped_widget, WidgetContainerListContentsMixin):
            raise ValueError("SearchableListBox must wrap ContainerListContentsMixin, wrapped is {}".format(type(wrapped_widget)))
        self.looked_field = looked_field
        self._search = ''

    def __getattr__(self, attr):
        return getattr(self._wrapped_widget, attr)

    def _set_search(self, new_search):
        """
        Update the search and the focus *only* if a field matches

        :param new_search: the new_searchable field
        :type new_search: str
        """
        #for index in self._w: #FIXME: see https://github.com/urwid/urwid/pull/201
        for index in self._w.__iter__():
            item = self._w[index]
            if self.looked_field(item).startswith(new_search):
                self._search = new_search
                self.set_focus(index)
                self._invalidate()
                break

    search = property(lambda self: self._search, _set_search, doc="""
    The looked string

    .. note:: this string is updated *only* if it matches
    """)

    def keypress(self, size, key):
        """
        Capture the key that may be used for searching item
        """
        key = super().keypress(size, key)
        if key is None:
            # Clear the search if key was used for something else
            self._search = ''
            return key
        if key == 'backspace':
            if self.search:
                self.search = self.search[:-1]
        elif len(key) == 1:
            self.search = self.search + key
        else:
            # Clear the search if key is not a character
            self._search = ''
            return key



def _test():
    import doctest
    doctest.testmod()

if __name__=='__main__':
    _test()
