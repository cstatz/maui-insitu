# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.mesh import CartesianMesh
from maui.field import ScalarField
from mauiinsitu import MauiInSitu
from maui import logger

logger = logger.getChild(__file__.strip().split('/')[-1].split('.')[0])

# Create a 3d cartesian mesh
logger.info("Setting up mesh.")
mesh_bounds = ((-50., -50., -50.), (50., 50., 50.))
discretization = 0.5
mesh = CartesianMesh(mesh_bounds, discretization)

# Create scalar field g from the mesh
logger.info("Creating field.")
g = ScalarField(mesh, "g", "nounit")
g.sync()

# Initialize parts of the fields with some values
g[50:60, 20:, :] = 3.
g.sync()

# Create the output
logger.info("Instantiating IO.")
io = MauiInSitu([g], "example_insitu", ".")

# Write the output
logger.info("Running simulation.")
io.run()
