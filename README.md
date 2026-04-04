# Deterministic Code Generation

Most code generation tools focus on producing code.

This project is about something else:

**preserving architecture.**

---

## The Problem

Many systems start clean and understandable, then degrade over time.

Not because the code is bad, but because the structure is not enforced.

- components grow organically  
- interfaces drift  
- patterns are copied inconsistently  
- architectural intent is lost  

The result is a system that *works*, but cannot be reasoned about.

---

## The Idea

Instead of writing system structure directly in C++, we describe it at a higher level:

- what data exists  
- how that data flows  
- which components process it  

Then we generate the implementation.


The generator is deterministic:

- same input → same output  
- no hidden behavior  
- no runtime framework  

The generated code is just **plain C++**.

---

## What This Repository Contains

This repository contains two example generators:

### SimpleGenerator
A minimal example showing:

- YAML model input  
- Jinja2 templates  
- generated C++ types  

This is the starting point.

---

### SerializationGenerator
Builds on the simple model to generate:

- measurement types  
- binary serialization (BDS-style)  
- debugging/logging (`operator<<`)  

This demonstrates how repetitive, error-prone code can be generated consistently.

---

## Why This Approach

This is not an IDL.

It does not generate code for a runtime system.

Instead:

- the model describes the **system itself**
- the generator produces **final implementation code**
- the result is explicit, readable, and debuggable

There is:

- no reflection  
- no schema interpreter  
- no hidden allocation  

Just C++.

---

## Example

A small model:

```yaml
measurements:
  - Temperature
  - Humidity

queues:
  - TemperatureQueue

stages:
  - TemperatureSensor
  - Logger

connections:
  - from: TemperatureSensor
    to: TemperatureQueue
  - from: TemperatureQueue
    to: Logger

## Getting Started
1. Install dependencies
      pip install pyyaml jinja2
2. Run a generator
      cd SimpleGenerator
      ./generator.py

Generated code will be written to the output directory.
