Ostinato
========

A simple program which generates the accompaniment based on a given melody.

Usage
-----

Input a 

```
from ostinato import Ostinato

ly = Ostinato("input.ly")
ly.generate_lh()
print ly.output()
```

Requirements
------------

*  `python-ly` 

Sample Usage
------------

```py
mary_had_a_little_lamb = r"""  \relative c'
{

\time 4/4
e d c d
e e e2
d4 d d2
e4 g g2
e4 d c d
e e e e
d d e d
c1
}
"""

show(ostinato(mary_had_a_little_lamb))
```

The original lilypond file would be:

![Mary had a little lamb](https://raw.githubusercontent.com/chappers/chappers.github.com/master/img/ostinato/marylamb.png)

whilst the updated one would be:

![Mary had a little lamb](https://raw.githubusercontent.com/chappers/chappers.github.com/master/img/ostinato/marylamb-lh.png)