#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'Christoph Statz'

import logging
from maui.mesh import RectilinearMesh
from maui.field import ScalarField, VectorField, TensorField
from visitor import VISIT_VARTYPE_VECTOR, VISIT_VARTYPE_SCALAR, VISIT_VARTYPE_TENSOR, \
    VISIT_VARCENTERING_NODE, VISIT_MESHTYPE_RECTILINEAR


var_type_map = {TensorField: VISIT_VARTYPE_TENSOR, VectorField: VISIT_VARTYPE_VECTOR, ScalarField: VISIT_VARTYPE_SCALAR}
axes_letters = ['x', 'y', 'z']


class MeshDataProvider(object):

    def __init__(self, mesh):
        self.logger = logging.getLogger(__name__)
        self.__mesh = mesh

    def __call__(self, *args, **kwargs):
        self.logger.debug("Providing data for mesh.")
        return tuple(self.__mesh.axes)


class VarDataProvider(object):

    def __init__(self, data):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(type(data))
        self.__data = data

    def __call__(self, *args, **kwargs):
        self.logger.debug("Providing data for variable.")
        return self.__data


class InSituDataAdapter(object):

    def __init__(self, fields):

        self.logger = logging.getLogger(__name__)

        self.__fields = fields
        self.__variables = dict()
        self.__meshes = dict()

        for field in fields:

            if len(field.d) > 1:
                logger.error("Currently InSitu only provides support for 1 domain per processor.")
                raise ValueError("Currently InSitu only provides support for 1 domain per processor.")

            if not isinstance(field.partition.mesh, RectilinearMesh):
                logger.error("Currently only fields associated with a rectilinear mesh are supported: %s !" % field.name)
                raise TypeError("Currently only fields associated with a rectilinear mesh are supported: %s !" % field.name)

            mesh_name = field.name + "_mesh"
            self.__meshes[mesh_name] = dict()
            self.__meshes[mesh_name]['mesh_type'] = VISIT_MESHTYPE_RECTILINEAR

            for key in field.d:
                logger.debug("Mesh for domain: %s" % str(key))
                self.__meshes[mesh_name]['data_provider'] = MeshDataProvider(field.partition.domains[key].mesh)
            self.__meshes[mesh_name]['dimension'] = field.partition.mesh.dimension

            self.__meshes[mesh_name]['kwargs'] = dict()

            for i in range(field.partition.mesh.dimension):
                self.__meshes[mesh_name]['kwargs'][axes_letters[i]+'label'] = field.partition.mesh.axes_names[i]
                self.__meshes[mesh_name]['kwargs'][axes_letters[i]+'units'] = field.partition.mesh.unit

            self.__variables[field.name] = dict()
            self.__variables[field.name]['mesh_name'] = mesh_name
            self.__variables[field.name]['var_type'] = var_type_map[type(field)]
            self.__variables[field.name]['centering'] = VISIT_VARCENTERING_NODE

            self.__variables[field.name]['kwargs'] = dict()
            self.__variables[field.name]['kwargs']['units'] = field.unit

            for key in field.d:
                logger.debug("Variable for domain: %s" % str(key))
                self.__variables[field.name]['data_provider'] = VarDataProvider(field.d[key])

    @property
    def meshes(self):
        return self.__meshes

    @property
    def variables(self):
        return self.__variables
