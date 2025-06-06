# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This package defines the CGS units.  They are also available in
(and should be used through) the `astropy.units` namespace.
"""
# avoid ruff complaints about undefined names defined by def_unit
# ruff: noqa: F821

from fractions import Fraction

import numpy as np

from . import si
from .core import UnitBase, def_unit
from .docgen import generate_unit_summary

__all__: list[str] = []  #  Units are added at the end

_ns = globals()

cm = si.cm
g = si.g
s = si.s
C = si.C
rad = si.rad
sr = si.sr
cd = si.cd
K = si.K
deg_C = si.deg_C
mol = si.mol


##########################################################################
# ACCELERATION

def_unit(
    ["Gal", "gal"],
    cm / s**2,
    namespace=_ns,
    prefixes=True,
    doc="Gal: CGS unit of acceleration",
)


##########################################################################
# ENERGY

# Use CGS definition of erg
def_unit(
    ["erg"],
    g * cm**2 / s**2,
    namespace=_ns,
    prefixes=True,
    doc="erg: CGS unit of energy",
)


##########################################################################
# FORCE

def_unit(
    ["dyn", "dyne"],
    g * cm / s**2,
    namespace=_ns,
    prefixes=True,
    doc="dyne: CGS unit of force",
)


##########################################################################
# PRESSURE

def_unit(
    ["Ba", "Barye", "barye"],
    g / (cm * s**2),
    namespace=_ns,
    prefixes=True,
    doc="Barye: CGS unit of pressure",
)


##########################################################################
# DYNAMIC VISCOSITY

def_unit(
    ["P", "poise"],
    g / (cm * s),
    namespace=_ns,
    prefixes=True,
    doc="poise: CGS unit of dynamic viscosity",
)


##########################################################################
# KINEMATIC VISCOSITY

def_unit(
    ["St", "stokes"],
    cm**2 / s,
    namespace=_ns,
    prefixes=True,
    doc="stokes: CGS unit of kinematic viscosity",
)


##########################################################################
# WAVENUMBER

def_unit(
    ["k", "Kayser", "kayser"],
    cm**-1,
    namespace=_ns,
    prefixes=True,
    doc="kayser: CGS unit of wavenumber",
)


###########################################################################
# ELECTRICAL

def_unit(
    ["D", "Debye", "debye"],
    Fraction(1, 3) * 1e-29 * C * si.m,
    namespace=_ns,
    prefixes=True,
    doc="Debye: CGS unit of electric dipole moment",
)
def_unit(
    ["Fr", "Franklin", "statcoulomb", "statC", "esu"],
    g ** Fraction(1, 2) * cm ** Fraction(3, 2) * s**-1,
    namespace=_ns,
    doc="Franklin: CGS (ESU) unit of charge",
)
def_unit(
    ["statA", "statampere"],
    Fr * s**-1,
    namespace=_ns,
    doc="statampere: CGS (ESU) unit of current",
)
def_unit(
    ["Bi", "Biot", "abA", "abampere"],
    g ** Fraction(1, 2) * cm ** Fraction(1, 2) * s**-1,
    namespace=_ns,
    doc="Biot: CGS (EMU) unit of current",
)
def_unit(
    ["abC", "abcoulomb"],
    Bi * s,
    namespace=_ns,
    doc="abcoulomb: CGS (EMU) of charge",
)

###########################################################################
# MAGNETIC

def_unit(
    ["G", "Gauss", "gauss"],
    1e-4 * si.T,
    namespace=_ns,
    prefixes=True,
    doc="Gauss: CGS unit for magnetic field",
)
def_unit(
    ["Mx", "Maxwell", "maxwell"],
    1e-8 * si.Wb,
    namespace=_ns,
    doc="Maxwell: CGS unit for magnetic flux",
)
def_unit(
    ["Oe", "Oersted", "oersted"],
    1e3 / (4 * np.pi) * si.A / si.m,
    namespace=_ns,
    prefixes=True,
    doc="Oersted: CGS unit for magnetic field strength",
)


###########################################################################
# BASES

bases = {cm, g, s, rad, cd, K, mol}


###########################################################################
# ALL & DOCSTRING

__all__ += [n for n, v in _ns.items() if isinstance(v, UnitBase)]

if __doc__ is not None:
    # This generates a docstring for this module that describes all of the
    # standard units defined here.
    __doc__ += generate_unit_summary(globals())
