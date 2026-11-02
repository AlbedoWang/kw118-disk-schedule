from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Policy(Enum):
    FCFS = "fcfs"
    SSTF = "sstf"
    SCAN = "scan"


class Direction(Enum):
    UP = "up"
    DOWN = "down"


class Tool(Enum):
    COMPUTE = "schedule_requests"
    SAVE = "save_result"


class Task(Enum):
    RUN = "disk-schedule"


@dataclass
class ComputeInput(Output):
    cylinders: Annotated[int, "cylinders"]
    head: Annotated[int, "head"]
    requests: Annotated[list[int], "requests"]
    policy: Annotated[Policy, "policy"]
    direction: Annotated[Direction, "direction"]


@dataclass
class ComputeOutput(Output):
    order: Annotated[list[int], "order"]
    path: Annotated[list[int], "path"]
    movement: Annotated[int, "movement"]


@dataclass
class SaveInput(Output):
    result: Annotated[ComputeOutput, "result"]


@dataclass
class SaveOutput(Output):
    path: Annotated[str, "path"]
    result: Annotated[ComputeOutput, "result"]


TOOLS = {Tool.COMPUTE: (ComputeInput, ComputeOutput), Tool.SAVE: (SaveInput, SaveOutput)}
TASKS = {Task.RUN: (ComputeInput, SaveOutput)}
