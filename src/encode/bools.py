from z3 import BoolRef, Bool
from typing import List, Iterable, Dict
from tqdm import tqdm

from src.package import PackageReference, PackageGroup
from src.debug import in_debug

BoolGroup = Dict[PackageReference, BoolRef]


def to_bools(repository: PackageGroup,
             time_range: Iterable[int]) -> List[BoolGroup]:
    return [{
        reference: to_bool(reference, time_step) for reference in repository
    } for time_step in tqdm(time_range, disable=in_debug())]


def to_bool(reference: PackageReference, time_step: int) -> Bool:
    return Bool('%s_%i' % (reference, time_step))
