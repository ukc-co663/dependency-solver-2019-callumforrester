from z3 import ModelRef
from typing import Iterable, Any

from src.package import Command, CommandSort, PackageGroup
from src.encode import BoolRepository, neighbours, BoolGroup


def decode(model: ModelRef, bools: BoolRepository,
           repository: PackageGroup) -> Iterable[Command]:
    all_commands = (to_command(model, from_state, to_state)
                    for from_state, to_state in neighbours(bools))

    return list(filter(is_not_none, all_commands))


def to_command(model: ModelRef, before: BoolGroup,
               after: BoolGroup) -> Command:
    for p in before.keys():
        installed_before = bool(model.eval(before[p]))
        installed_after = bool(model.eval(after[p]))

        if (not installed_before) and installed_after:
            return Command(CommandSort.INSTALL, p)
        elif installed_before and (not installed_after):
            return Command(CommandSort.UNINSTALL, p)
    return None


def is_not_none(a: Any) -> bool:
    return a is not None
