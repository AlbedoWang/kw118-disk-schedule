# kw118-disk-schedule

An original COMP 480/580 verifiable systems task by Kaijian Wang (kw118).

## Tools

| Tool/task | Behavior |
|---|---|
| `schedule_requests` | Compute the exact typed domain result. |
| `save_result` | Accept a ComputeOutput as result; write result.json and return path plus result. |
| `disk-schedule` | Agent task: compute, save, then submit the saved output unchanged. |

### Rules and output semantics

All requests arrive at time zero. cylinders>0; head and requests in [0,cylinders). order contains original zero-based request indices, including duplicates separately. path starts with head and includes each service location and any required SCAN endpoint. FCFS uses input order. SSTF ties use smaller cylinder then smaller input index. SCAN serves current-head requests first in input order and travels up/down. If requests remain on the opposite side, visit the physical endpoint before reversing. Stop when the last request is serviced; do not finish an unnecessary sweep. Empty queue path=[head]. direction is required but ignored for FCFS/SSTF. movement is the sum of absolute adjacent path differences, not elapsed time.

The input/output field shapes and Enum values are declared in contract.py. Invalid semantic inputs raise ValueError (except malformed packet contents, which the inspection task reports explicitly). No model is used to judge results. The verifier independently recomputes the expected answer, compares every result field, and reads the actual result.json. A matching declaration alone is insufficient. Acceptance is binary; the framework score is 1 for valid and 0 for invalid.

### Example task input

```json
{
  "cylinders": 200,
  "head": 53,
  "requests": [
    98,
    183,
    37,
    122,
    14,
    124,
    65,
    67,
    53,
    37
  ],
  "policy": "fcfs",
  "direction": "up"
}
```

In RUSH Lab, request the `disk-schedule` task with this structured input. The agent calls `schedule_requests`, passes its complete output to save_result, and submits the saved output. A model and RUSH Lab access are needed for this step; pytest does not establish agent success.

## Layout

- contract.py: typed tools, task and outputs.
- src/plugin/: MCP server, computation and file saving.
- verifier/: independent deterministic oracle and artifact checks.
- tests/: public pedagogical task inputs and regression checks, not experiment logs.
- ui/ and product/: schema-based result display and marketplace metadata.

## Develop and run

Requires Git, uv and Python 3.12+. From this repository:

```sh
uv sync --frozen --extra dev --no-editable
uv run --frozen --no-editable pytest -q
uv run --frozen --no-editable ruff check .
uv lock --check
```

Normal (non-editable) installation is intentional: it also checks packaged source imports. After editing source, rerun uv sync with --reinstall-package nanoagent-kw118-disk-schedule. Do not copy another project's virtual environment.

The manifest's runtime remains the official `[uv, run, --frozen, python, -m, plugin]`. The host supplies NANOAGENT_WORKSPACE. No API keys or plugin network hosts are needed. All writes stay in the workspace. Existing symlink destinations are rejected. Runtime files, logs and the milestone report belong outside this repository.

### Validation and limitations

Tests cover the domain boundaries, wrong results, missing/malformed artifacts, schema failures and symlink protection. Fixtures are intentionally small public teaching inputs representing the actual task contract, not hardware performance samples. Tools and oracle use separate implementations. Local correctness does not establish marketplace installation or model behavior; those require recorded real platform runs.
