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
