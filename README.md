# ImmutableDict

How to Use:

```python
from immutabledict import ImmutableDict

items: list[tuple[str, str]] = [(f"Key{i}", f"Value{i}") for i in range(1, 21)]

D: ImmutableDict[str, str] = ImmutableDict(items)
for key, value in D.items():
    ... # your code

New: dict[str, str] = D.to_dict() # returns a shallow copy of the Dictonary as dic object
```