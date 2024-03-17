from __future__ import annotations

from collections.abc import (
    Mapping,
    KeysView,
    ValuesView,
    ItemsView,
)
import typing as t
import abc

KT = t.TypeVar("KT") # KT and VT would be covariant but that does not work
VT = t.TypeVar("VT")
T = t.TypeVar("T")

@t.runtime_checkable
class SupportsKeysAndGetItem(t.Protocol[KT, VT]):
    @abc.abstractmethod
    def __getitem__(self, key: KT) -> VT: pass
    @abc.abstractmethod
    def keys(self) -> KeysView[KT]: pass

class Immutable(object):
    def __hash__(self) -> int:
        return id(self)

    def __copy__(self):
        return self
    
    def __deepcopy__(self, memo):
        return self

class ImmutableDict(Immutable, Mapping[KT, VT]):
    """ImmutableDict"""
    @t.overload
    def __init__(self, __map: SupportsKeysAndGetItem[KT, VT]) -> None: pass
    @t.overload
    def __init__(self, __iter: t.Iterable[tuple[KT, VT]]) -> None: pass

    def __init__(self, other, /):
        """
        Examples
        .. code-block:: python

            >>> my_iter = [(chr(i), i) for i in range(1, 1001)]
            >>> a: ImmutableDict[str, int] = ImmutableDict(my_iter)

            >>> my_dict = {chr(i): i for i in range(1, 1001)} # same as my_iter
            >>> b: ImmutableDict[str, int] = ImmutableDict(my_dict)
            
            >>> a == my_iter
            True
            >>> b == a
            True
            >>> b == my_dict
            True
            >>> a == object()
            False"""
        v = dict(other)
        def _repr():
            return "ImmutableDict(%s)" % repr(v)

        object.__setattr__(self, "__getitem__", v.__getitem__)
        object.__setattr__(self, "__repr__", _repr)
        object.__setattr__(self, "__len__", v.__len__)
        object.__setattr__(self, "__iter__", v.__iter__)

    def __getitem__(self, key: KT) -> VT:
        return object.__getattribute__(self, "__getitem__")(key)
    
    def __repr__(self) -> str:
        return object.__getattribute__(self, "__repr__")()
    
    def __len__(self) -> int:
        return object.__getattribute__(self, "__len__")()
    
    def __iter__(self) -> t.Generator[KT, t.Any, None]:
        yield from object.__getattribute__(self, "__iter__")()
    
    def __reversed__(self) -> t.Generator[KT, t.Any, None]:
        yield from reversed(list(self))
    
    # copy of collections.abc.Mapping methods
    def __eq__(self, other) -> bool:
        try:
            is_eq = dict(other)
        except (ValueError, TypeError):
            return False
        else:
            return dict(self) == is_eq

    @t.overload
    def get(self, key: KT) -> t.Union[VT, None]: pass
    @t.overload
    def get(self, key: KT, default: T) -> t.Union[VT, T]: pass

    def get(self, key, default = None):
        """Immutabledict.get(key, default)
        
        Example
        .. code-block:: python
            
            >>> D = ImmutableDict({"Key": "Value"})
            >>> D.get("Key")
            'Value'
            >>> D.get("Key1")
            None
            >>> D.get("Key1", "Value1")
            'Value1'
            """
        try:
            return self[key]
        except KeyError:
            return default
    
    def keys(self) -> KeysView[KT]:
        return KeysView(self)
    
    def values(self) -> ValuesView[VT]:
        return ValuesView(self)

    def items(self) -> ItemsView[KT, VT]:
        return ItemsView(self)
    
    def to_dict(self) -> t.Dict[KT, VT]:
        """return a shallow copy of the dictionary as dict object"""
        return dict(self.items())