#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'Christoph Statz'

import logging

from maui.backend import context
from visitor import ParallelVisitInstrumentation, VisitInstrumentation
from .adapter import InSituDataAdapter


class MauiInSitu(object):

    def __init__(self, fields, identifier, *args, **kwargs):

        self.logger = logging.getLogger(__name__)
        self.logger.debug("Instantiating InSitu Visualization")

        description = "Maui Framework In-Situ Visualization."

        if hasattr(context, 'comm'):
            instrumentation = ParallelVisitInstrumentation(identifier, description, *args, **kwargs)
        else:
            instrumentation = VisitInstrumentation(identifier, description, *args, **kwargs)

        self.__instrumentation = instrumentation

        self.__data_adapter = InSituDataAdapter(fields)

        for name in self.__data_adapter.meshes:
            mesh_type = self.__data_adapter.meshes[name]['mesh_type']
            dimension = self.__data_adapter.meshes[name]['dimension']

            mesh_kwargs = dict()
            try:
                mesh_kwargs = self.__data_adapter.meshes[name]['kwargs']
            except KeyError:
                self.logger.warn("No metadata provided for mesh %s!" % name)

            if isinstance(self.__data_adapter.meshes[name]['domain_number'], dict):
                for key in self.__data_adapter.meshes[name]['domain_number']:
                    domain = self.__data_adapter.meshes[name]['domain_number'][key]
                    dp = self.__data_adapter.meshes[name]['data_provider'][key]
                    self.__instrumentation.register_mesh(name, dp, mesh_type, dimension, domain=domain, number_of_domains=self.__data_adapter.meshes[name]['number_of_domains'], **mesh_kwargs)
            else:
                self.__instrumentation.register_mesh(name, None, mesh_type, dimension, domain='omit', number_of_domains=self.__data_adapter.meshes[name]['number_of_domains'], **mesh_kwargs)

        for name in self.__data_adapter.variables:
            self.logger.debug(name)
            var_type = self.__data_adapter.variables[name]['var_type']
            var_centering = self.__data_adapter.variables[name]['centering']
            mesh_name = self.__data_adapter.variables[name]['mesh_name']

            var_kwargs = dict()

            try:
                var_kwargs = self.__data_adapter.variables[name]['kwargs']
            except KeyError:
                self.logger.warn("No metadata provided for variable %s!" % name)

            if isinstance(self.__data_adapter.variables[name]['domain_number'], dict):
                for key in self.__data_adapter.variables[name]['domain_number']:
                    domain = self.__data_adapter.variables[name]['domain_number'][key]
                    dp = self.__data_adapter.variables[name]['data_provider'][key]
                    self.__instrumentation.register_variable(name, mesh_name, dp, var_type, var_centering, domain=domain, **var_kwargs)
            else:
                self.__instrumentation.register_variable(name, mesh_name, None, var_type, var_centering, domain='omit', **var_kwargs)

    def register_curve(self, name, data_provider):
        self.__instrumentation.register_curve(name, data_provider)

    def register_expression(self, name, expr, var_type, **kwargs):
        self.__instrumentation.register_expression(name, expr, var_type, **kwargs)

    def register_ui_command(self, name, function, args):
        self.__instrumentation.register_ui_command(name, function, args)

    def register_ui_value(self, name, function, args):
        self.__instrumentation.register_ui_value(name, function, args)

    def register_ui_state(self, name, function, args):
        self.__instrumentation.register_ui_state(name, function, args)

    def register_ui_set_int(self, name, function):
        self.__instrumentation.register_ui_set_int(name, function)

    def register_ui_set_string(self, name, function):
        self.__instrumentation.register_ui_set_string(name, function)

    def register_command(self, name, function, args):
        self.__instrumentation.register_generic_command(name, function, args)

    def run(self):
        self.__instrumentation.run()

    def step_wrapper(self, step):
        return self.__instrumentation.step_wrapper(step)
