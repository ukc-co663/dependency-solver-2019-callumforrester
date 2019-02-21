from z3 import BoolRef, Not, Or, And
from typing import List, Set

from src.encode.bools import BoolGroup
from src.package.package import PackageGroup, PackageReference


def exact_installed(bools: BoolGroup,
                    installed_packages: Set[PackageReference]) -> BoolRef:
    return And([package_bool == (reference in installed_packages)
                for reference, package_bool in bools.items()])


def none_installed(bools: BoolGroup,
                   constraints: List[PackageGroup]) -> BoolRef:
    return Not(any_installed(bools, constraints))


def any_installed(bools: BoolGroup,
                  packages: PackageGroup) -> BoolRef:
    return Or(get_bools(bools, packages))


def get_bools(bools: BoolGroup, packages: PackageGroup) -> List[BoolRef]:
    return [bools[p] for p in packages]
