from invoke import Collection
from .gen import ns as gen

ns = Collection()
ns.add_collection(gen, name='gen')
