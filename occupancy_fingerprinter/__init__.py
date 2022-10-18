"""A tool to generate grid-based binding site shapes."""

# Add imports here
from .occupancy_fingerprinter import *

from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
