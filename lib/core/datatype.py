from lib.core.settings import ENCODE_NONE
import copy
import types


class AttribDict(dict):
    """
    This class defines the dictionary with added capability to access members as attributes
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("unable to access item '%s'" % item)

    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """

        # This test allows attributes to be set in the __init__ method
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        # Any normal attributes are handled normally
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal


class Position(object):
    def __init__(self):
        self._pos = None
        self._token = None
        self._line = None
        self._tag = None
        self._attr = None

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    @property
    def attr(self):
        return self._attr

    @attr.setter
    def attr(self, attr):
        self._attr = attr


class Payload(object):
    def __init__(self):
        self._func = None
        self._value = None
        self._trigger = None
        self._encode = ENCODE_NONE

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, func):
        self._func = func

    @property
    def encode(self):
        return self._encode

    @encode.setter
    def encode(self, encode):
        self._encode = encode

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def trigger(self):
        return self._trigger

    @trigger.setter
    def trigger(self, trigger):
        self._trigger = trigger

    def __str__(self):
        return self.value
