import pattern_search as ps
import numpy as np

def rosenbrock_func_gen(n=10, a=1, b=100):
    xs = np.linspace(-0.5, 2, n)
    ys = np.linspace(-1.0, 3, n)

    def f(i,j):
        if not (0 <= i < n and 0 <= j < n):
            return np.nan
        x = xs[i]; y = ys[j]
        return (a-x)**2+b*(y-x**2)**2

    return xs, ys, f

def custom_print(xs,ys,p,f):
    f_val = f(p.center.i,p.center.j)
    print(f"f({xs[p.center.i]:.2f},{ys[p.center.j]:.2f}) = {f_val:.4f}")



path = [] # [(center,step)...]
n = 2**10
step = (2**5,2**5)
center = (0,0)

xs, ys, f = rosenbrock_func_gen(n)
p = ps.Pattern(center, step, ps.empty_cache.copy())

maxiter = 50
minstep = (0,0)
maxcache = 200
niter = 0
while all([
    niter < maxiter,
    p.step[0] > minstep[0],
    p.step[1] > minstep[1],
    p.cache.dropna().size < maxcache
    ]):
    # print(p)
    custom_print(xs,ys,p,f)
    path.append(p.center)
    p.fill(f)
    # evolve! 81)
    p = p.update()
    niter += 1

## code for plotting
# %pylab
# p.cache.plot()
# path2 = p.cache.index.values.tolist()
# plt.plot(*zip(*path2))
# plt.plot(*zip(*path))
