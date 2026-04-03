# SerializationGenerator

This generator produces C++ measurement types and Binary Data Stream (BDS) serialization code from a simple YAML model.

It is part of the examples from:

[**Raising the Level of Abstraction: Deterministic Code Generation for C++**](https://leanpub.com/raisingthelevelofabstraction)

---

## Overview

This tool demonstrates a deterministic code generation approach:

- Input: a simple YAML model describing measurement types
- Output: plain C++ code
- No runtime schema
- No reflection
- No hidden allocation
- No frameworks

The generated code is intended to look exactly like what you would write by hand.

---

## Usage

```bash
./generator.py
```

This reads model.yaml and generates output files in:

```
generated/
```
The generator expects a YAML file with this structure:
```
output: generated

measurements:
  - name: Temperature
    fields:
      - name: value
        type: double
        bds_write: writeDouble
        bds_read: readDouble
```

Each measurement:

- has a name
- contains zero or more fields
  
each field defines:
- type
- serialization functions

Generated Output

The generator produces:
```
generated/
├── MeasurementTypes.h
├── BdsMeasurementCodecs.h
├── BdsMeasurementCodecs.cpp
├── MeasurementIO.h
├── MeasurementIO.cpp
MeasurementTypes.h
```

Plain C++ value types:
```
struct Temperature
{
    double value{};
};
```

BdsMeasurementCodecs

Explicit serialization functions:

BinaryWriteStream& writeTemperature(BinaryWriteStream& stream,
                                    const Temperature& measurement) noexcept
{
    stream.writeDouble(measurement.value);
    return stream;
}
MeasurementIO

Debug/logging support:

std::ostream& operator<<(std::ostream& os, const Temperature& value)
{
    os << "Temperature{value=" << value.value << "}";
    return os;
}
Design Philosophy

This generator is intentionally:

- simple
- explicit
- deterministic

It does not:

- introduce a runtime system
- interpret schemas dynamically
- hide behavior behind abstraction layers

Instead, it produces:

Plain C++ code that becomes part of your system

Why This Exists

Many parts of embedded and systems software are:

- repetitive
- mechanical
- error-prone

Examples:

- data types
- serialization code
- logging/debugging output

This generator removes that repetition while preserving:

- control
- clarity
- performance
- analyzability
- Relationship to Other Generators

This repository also contains a simpler generator (simplegenerator) that
produces system structure (pipelines, queues, stages).

This generator focuses only on:

- data types
- serialization
- debugging support

Generators are intentionally kept small and focused.

Notes
The YAML format is a convenience, not the abstraction itself
The model represents system concepts, not C++ constructs
The generator is deterministic: same input → same output
