import json, inspect
from collections import defaultdict
from pathlib import Path


def print_pretty(obj):
    print(json.dumps(obj, indent=2))


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


def generate(key, grouped_projects, header):
    lines = []
    # TODO: Sort group by custom order
    for group_name, group in grouped_projects.items():
        lines.append("\n<br>\n")
        lines.append(f"### {group_name}")        
        for project in sorted(group, key=lambda x: x["name"]):
            name = project["name"]
            link = project["link"]
            description = project["description"]
            affiliations = '|'.join(project["affiliations"])
            platforms = '|'.join(project["platforms"])
            languages = ' '.join(f'`{x}`' for x in project["languages"])
            primary_language = project["primaryLanguage"]
            types = '|'.join(project["types"])
            technologies = ' '.join(f'`{x}`' for x in project["technologies"])
            tags = ' '.join(f'`{x}`' for x in project["tags"])            
            line = f"#### [{name}]({link}) &#8212; {description}"
            lines.append(line)
            # TODO: deal with Other
            line = f"`affl:{affiliations}` " if key != 'affiliations' and affiliations != "Other" else ''
            line += f"`type:{types}` " if key != 'types' and types != "Other" else ''
            line += f"`{primary_language}` " if key != 'primaryLanguage' and primary_language != "Other" else ''
            line += f"`{platforms}` " if key != 'platforms' and platforms != primary_language  and platforms != "Other" else ''
            line += f"{technologies} {tags}"
            lines.append(line)

    content = "{0}\n{1}".format(header, '\n\n'.join(lines))
    return content


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