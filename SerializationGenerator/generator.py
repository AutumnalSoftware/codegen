#!/usr/bin/python3

import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def validate_model(model):
    measurements = model.get('measurements', [])

    if not isinstance(measurements, list):
        raise ValueError("measurements must be a list")

    seen_names = set()

    for m in measurements:
        if not isinstance(m, dict):
            raise ValueError("each measurement must be a mapping")

        name = m.get('name')
        if not name:
            raise ValueError("each measurement must have a name")

        if name in seen_names:
            raise ValueError(f"Duplicate measurement name: {name}")
        seen_names.add(name)

        fields = m.get('fields', [])
        if not isinstance(fields, list):
            raise ValueError(f"fields for measurement '{name}' must be a list")

        field_names = set()

        for f in fields:
            if not isinstance(f, dict):
                raise ValueError(f"each field in measurement '{name}' must be a mapping")

            field_name = f.get('name')
            field_type = f.get('type')

            if not field_name:
                raise ValueError(f"a field in measurement '{name}' is missing a name")

            if field_name in field_names:
                raise ValueError(
                    f"Duplicate field name '{field_name}' in measurement '{name}'"
                )
            field_names.add(field_name)

            if not field_type:
                raise ValueError(
                    f"field '{field_name}' in measurement '{name}' is missing a type"
                )

            # Empty is allowed to have no fields.
            if name != 'Empty':
                if 'bds_write' not in f:
                    raise ValueError(
                        f"field '{field_name}' in measurement '{name}' is missing bds_write"
                    )
                if 'bds_read' not in f:
                    raise ValueError(
                        f"field '{field_name}' in measurement '{name}' is missing bds_read"
                    )

def main():
    with open('model.yaml', 'r') as yaml_file:
        model = yaml.safe_load(yaml_file)

    validate_model(model)

    env = Environment(
        loader=FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True
    )

    output_dir = Path(model.get('output', 'generated'))
    output_dir.mkdir(parents=True, exist_ok=True)

    files_to_generate = [
        ('measurements.h.j2', output_dir / 'MeasurementTypes.h'),
        ('bds_measurement_codecs.h.j2', output_dir / 'BdsMeasurementCodecs.h'),
        ('bds_measurement_codecs.cpp.j2', output_dir / 'BdsMeasurementCodecs.cpp'),
    ]

    for template_name, output_path in files_to_generate:
        template = env.get_template(template_name)
        output = template.render(model=model)

        with open(output_path, 'w') as f:
            f.write(output)

if __name__ == "__main__":
    main()
