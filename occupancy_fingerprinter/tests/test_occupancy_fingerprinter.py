"""
Unit and regression test for the occupancy_fingerprinter package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import occupancy_fingerprinter
from occupancy_fingerprinter import BindingSite
from occupancy_fingerprinter import Grid

import numpy as np
import mdtraj as md
import h5py as h5
import os
from pathlib import Path

cwd = Path.cwd()
mod_path = Path(__file__).parent


def test_occupancy_fingerprinter_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "occupancy_fingerprinter" in sys.modules

def test_binding_site_init():
    """Test binding site init"""
    center = np.array([10.,10.,10.])
    r = 5.
    spacing = np.array([1., 1., 1.])
    b = BindingSite(center, r, spacing)
    grid_x, grid_y, grid_z = b._cal_grid_coordinates()
    assert (b._center == center).all()
    assert b._r == r 
    assert (b._spacing == spacing).all()
    assert (b._counts == b.get_grid_counts()).all()
    assert (b._origin == b.get_origin()).all()
    assert (b._grid_x == grid_x).all()
    assert (b._grid_y == grid_y).all()
    assert (b._grid_z == grid_z).all()
    assert (b._upper_most_corner_crd == (b._center + ((b._counts - 1) * b._spacing)/2)).all()
    assert (b._upper_most_corner == (b._counts - 1)).all()
    assert (b._size == np.prod(b._counts))

def test_grid_init():
    traj_path = (mod_path / "../data/CLONE0.xtc").resolve()
    top_path = (mod_path / "../data/prot_masses.pdb").resolve()
    t = md.load(traj_path, top=top_path)
    t = t[:1]
    center = np.array([58., 73., 27.])
    r = 3.
    spacing = np.array([1., 1., 1.])
    g = Grid(t)
    assert g._n_sites == 0
    assert g._sites == {}
    g.add_binding_site(center, r, spacing)
    b = BindingSite(center,r,spacing)
    assert g._n_sites == 1
    assert (g._sites[0]._center == b._center).all()
    assert g._sites[0]._r == b._r
    assert (g._sites[0]._spacing == b._spacing).all()
    h5_path = (mod_path / "../data/test.h5").resolve()
    a = g.cal_fingerprint(h5_path, n_tasks=1, return_array=True)
    assert (a.sum() == 113)
    #check h5 file integrity
    with h5.File(h5_path, "r") as f:
        k = list(f.keys())
        assert k[0] == "frames"
        assert (f[k[0]] == a[0]).all()
    #test process_trajectory function
    p = occupancy_fingerprinter.process_trajectory(t,g._sites,g._atom_radii)
    assert (a == p).all()
    #test writing dx files
    dx_path = (mod_path / "../data/binding_site_test.dx").resolve()
    c = a[0].reshape(tuple(b._counts))
    b.write(dx_path, c)
    assert os.path.exists(dx_path)

def test_cal_fingerprint():
    traj_path = (mod_path / "../data/CLONE0.xtc").resolve()
    top_path = (mod_path / "../data/prot_masses.pdb").resolve()
    t = md.load(traj_path, top=top_path)
    t = t[:1]
    center = np.array([58., 73., 27.])
    r = 3.
    spacing = np.array([1., 1., 1.])
    g = Grid(t)
    g.add_binding_site(center, r, spacing)
    g.cal_fingerprint(None, n_tasks=0)
    g.cal_fingerprint(None, n_tasks=999)






