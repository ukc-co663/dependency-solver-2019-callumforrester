from functools import partial
from typing import List

from solver.package.package import Package, PackageReference, PackageGroup, Repository
from solver.flatten import flatten_as_list


def expand_repository(repository: Repository) -> PackageGroup:
    result = {}
    for name, packages in repository.items():
        for reference, package in packages.items():
            result[reference] = expand_package(repository, package)
    return result


def expand_package(repository: Repository, package: Package) -> Package:
    expand = partial(expand_reference, repository)
    expanded_dependencies = expand_dependencies(repository,
                                                package.dependencies)
    expanded_conflicts = flatten_as_list(map(expand, package.conflicts))
    return Package(package.size, expanded_dependencies, expanded_conflicts)


def expand_dependencies(repository: Repository,
                        dependencies: List[List[PackageReference]]) -> List[List[PackageGroup]]:
    expand = partial(expand_reference, repository)
    return list(map(lambda d: flatten_as_list(map(expand, d)),
                                                           dependencies))


def expand_reference(repository: Repository,
                     reference: PackageReference) -> PackageGroup:
    name = reference.name
    if name in repository:
        candidates = repository[reference.name]
        return filter(reference.compare, candidates)
    else:
        return iter(())
