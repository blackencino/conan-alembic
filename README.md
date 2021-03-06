# conan-alembic
Conan package for Alembic library

from: http://www.alembic.io/

Alembic is an open computer graphics interchange framework. Alembic
distills complex, animated scenes into a non-procedural,
application-independent set of baked geometric results. This
'distillation' of scenes into baked geometry is exactly analogous to
the distillation of lighting and rendering scenes into rendered image
data.

Alembic is focused on efficiently storing the computed results of
complex procedural geometric constructions. It is very specifically
NOT concerned with storing the complex dependency graph of procedural
tools used to create the computed results. For example, Alembic will
efficiently store the animated vertex positions and animated
transforms that result from an arbitrarily complex animation and
simulation process which could involve enveloping, corrective shapes,
volume-preserving simulations, cloth and flesh simulations, and so
on. Alembic will not attempt to store a representation of the network
of computations (rigs, basically) which are required to produce the
final, animated vertex positions and animated transforms.
