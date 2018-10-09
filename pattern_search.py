"""Minimize a function over a 2D grid
with a square pattern search"""
import pandas as pd
import numpy as np
from collections import namedtuple


grid_pt = namedtuple('grid_pt','i j')


class PatternError(Exception):
    """Some proble with the pattern"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


empty_cache = pd.DataFrame(columns = ['f_val'],
        index = pd.MultiIndex.from_arrays(
            [[],[]],
            names = ['i','j']
        )
    )


class Pattern:
    def __init__(self, center, step, cache=None):
        self.center = grid_pt(*center)
        self.step = grid_pt(*step)
        self.a = np.vstack([[-1,0,1]]*3)
        self.b = self.a.T
        self.i = self.center.i + self.a * self.step.i
        self.j = self.center.j + self.b * self.step.j
        self.df = pd.DataFrame({
                'i': self.i.ravel(),
                'j': self.j.ravel(),
                'f_val': np.nan
            }, index = pd.MultiIndex.from_arrays(
                [self.a.ravel(), self.b.ravel()],
                names = ['a','b']
            ))
        if cache is None:
            self.cache = empty_cache.copy()
        else:
            self.cache = cache

    def __repr__(self):
        return "Pattern("+str(self.center)+","+str(self.step)+")"

    def fill(self,f):
        for row in self.df.itertuples():
            # retrieve from cache or evaluate
            try:
                newf = self.cache.loc[(row.i,row.j),'f_val']
            except KeyError:
                newf = f(row.i,row.j)
                self.cache.loc[(row.i,row.j),'f_val'] = newf
            # set
            self.df.loc[row.Index,'f_val'] = newf

    def update(self):
        first = self.df.f_val.idxmin()
        if pd.isnull(first):
            raise PatternError(self)
        if first == (0,0):
            # shrink
            newcenter = self.center
            newstep = map(lambda x: x//2, self.step)
        elif first in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            # grow
            newstep = map(lambda x: x*2, self.step)
            newcenter = self.df.loc[first,['i','j']].astype(int)
        else:
            # move
            newcenter = self.df.loc[first,['i','j']].astype(int)
            newstep = self.step
        return Pattern(newcenter,newstep,self.cache)

