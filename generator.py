#!/usr/bin/python3

import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def validate_model(model):
    stages = set(model.get('stages', []))
    queues = set(model.get('queues', []))

    for c in model.get('connections', []):
        src = c['from']
        dst = c['to']

        if src not in stages and src not in queues:
            raise ValueError(f"Unknown source: {src}")

        if dst not in stages and dst not in queues:
            raise ValueError(f"Unknown destination: {dst}")


def render_measurements(model, output_dir):
    # Prepare the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True)
    template = env.get_template('measurements.h.j2')

    # Render the template with data from the YAML file
    output = template.render(model=model)

    # Save the rendered output to a file
    #with open('output/measurements.h', 'w') as cpp_file:
    with open(output_dir / 'measurements.h', 'w') as cpp_file:
        cpp_file.write(output)

    print("Generated measurements.h successfully.")

def render_queues(model, output_dir):
    # Prepare the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True)
    template = env.get_template('queues.h.j2')

    # Render the template with data from the YAML file
    #output = template.render(queues=model['queues'])
    output = template.render(model=model)

    # Save the rendered output to a file
    with open(output_dir / 'queues.h', 'w') as cpp_file:
        cpp_file.write(output)

    print("Generated queues.h successfully.")

def render_stages(model, output_dir):
    # Prepare the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True)
    template = env.get_template('stages.h.j2')

    # Render the template with data from the YAML file
    output = template.render(model=model)

    # Save the rendered output to a file
    with open(output_dir / 'stages.h', 'w') as cpp_file:
        cpp_file.write(output)

    print("Generated stages.h successfully.")

def render_pipelines(model, output_dir):
    # Prepare the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True)
    template = env.get_template('pipelines.h.j2')

    # Render the template with data from the YAML file
    output = template.render(model=model)

    # Save the rendered output to a file
    with open(output_dir / 'pipeline.h', 'w') as cpp_file:
        cpp_file.write(output)

    print("Generated pipeline.h successfully.")

def main():
    # Load the YAML file
    with open('model.yaml', 'r') as yaml_file:
        model = yaml.safe_load(yaml_file)
    validate_model(model)

    output_dir = Path(model.get('output', 'generated'))
    output_dir.mkdir(parents=True, exist_ok=True)

    render_measurements(model, output_dir)

    render_queues(model, output_dir)

    render_stages(model, output_dir)

    render_pipelines(model, output_dir)

if  __name__ == "__main__":
    main();
