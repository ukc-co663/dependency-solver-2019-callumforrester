import logging

from z3 import BoolRef, And, Implies
from typing import List, Optional
from tqdm import tqdm

from src.encode.state import EncodedState
from src.package.package import Package, PackageReference, PackageGroup
from src.debug import in_debug
from src.encode.install import none_installed, any_installed


def all_states_valid(states: List[EncodedState],
                     repository: PackageGroup) -> BoolRef:
    logging.debug('relationships constraint')

    constraints = [state_valid(b, i, p)
                   for i, p in tqdm(repository.items(), disable=in_debug())
                   for b in states]
    return And(constraints)


def state_valid(state: EncodedState,
                reference: PackageReference,
                package: Package) -> Optional[BoolRef]:
    installed = state[reference]
    return Implies(installed, relationships_satisfied(state, package))


def relationships_satisfied(state: EncodedState, package: Package) -> BoolRef:
    return And([dependencies_satisfied(state, package)
                if package.dependencies else True,
                conflicts_not_installed(state, package)
                if package.conflicts else True])


def dependencies_satisfied(state: EncodedState, package: Package) -> BoolRef:
    return And([any_installed(state, ds) for ds in package.dependencies])


def conflicts_not_installed(state: EncodedState, package: Package) -> BoolRef:
    return none_installed(state, package.conflicts)
