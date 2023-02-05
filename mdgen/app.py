import json, inspect
from collections import defaultdict

from pathlib import Path


def print_pretty(obj):
    print(json.dumps(obj, indent=2))


def generate(key, grouped_projects, header):
    lines = []
    for group_name, group in grouped_projects.items():
        lines.append("\n<br>\n")
        lines.append(f"### {group_name.upper()}")
        for project in group:
            name = project["name"]
            link = project["link"]
            description = project["description"]
            affiliations = ' '.join(f'`{x}`' for x in project["affiliations"])
            platforms = ' '.join(f'`{x}`' for x in project["platforms"])
            languages = ' '.join(f'`{x}`' for x in project["languages"])
            primary_language = f'`{project["primaryLanguage"]}`'
            types = ' '.join(f'`{x}`' for x in project["types"])
            technologies = ' '.join(f'`{x}`' for x in project["technologies"])
            tags = ' '.join(f'`{x}`' for x in project["tags"])
            
            line = f"#### [{name}]({link}) &#8212; {description}"
            lines.append(line)
            line = f"{affiliations} " if key != 'affiliations' and affiliations != "`Other`" else ''
            line += f"{types} " if key != 'types' and types != "`Other`" else ''
            line += f"{primary_language} " if key != 'primaryLanguage' and primary_language != "`Other`" else ''
            line += f"{platforms} " if key != 'platforms' and platforms != primary_language  and platforms != "`Other`" else ''
            line += f"{technologies} {tags}"
            lines.append(line)

    content = "{0}\n{1}".format(header, '\n\n'.join(lines))
    return content


def load_projects():
    with open("projects.json", "r") as file:
        projects = json.load(file)
    return projects


def group_by(key, projects):
    grouped = defaultdict(list)
    for project in projects:
        group_keys = [project[key]] if isinstance(project[key], str) else project[key]
        for group_key in group_keys:
            grouped[group_key].append(project)
    return grouped


def main():
    projects = load_projects()
    keys = ["primaryLanguage", "affiliations", "types", "platforms"]    
    index = 'primaryLanguage'
    index_alt = 'Language'

    for key in keys:
        grouped_projects = group_by(key, projects)
        
        header = inspect.cleandoc(f"""
            ---
            layout: default
            title: Shovra Das
            file: {key if key != index else 'index'}
            nav: By{key.title() if key != index else index_alt}
            ---
        """)
        
        content = generate(key, grouped_projects, header)
        
        Path('./pages').mkdir(exist_ok=True, parents=True)        
        with open(f"pages/{key if key != index else 'index'}.md", "w") as file:
            file.write(content)    


if __name__ == "__main__":
    main()