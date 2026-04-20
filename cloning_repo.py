from pydriller import Repository
import re
REPO_PATH = "./camel"
ISSUES = ["CAMEL-180", "CAMEL-321", "CAMEL-1818", "CAMEL-3214", "CAMEL-18065"]

pattern = re.compile("|".join(ISSUES))
total_commits = 0
total_files = 0
total_dmm = 0.0
for commit in Repository(REPO_PATH).traverse_commits():

    msg = commit.msg or ""
    if not pattern.search(msg):
        continue

    total_commits += 1

    files = set()
    unit_size = 0
    complexity = 0
    interfacing = 0

    for mod in commit.modified_files:

        if mod.new_path:
            files.add(mod.new_path)
        if mod.old_path:
            files.add(mod.old_path)

        unit_size += (mod.added_lines or 0) + (mod.deleted_lines or 0)
        complexity += (mod.complexity or 0)
        interfacing += len(mod.changed_methods) if mod.changed_methods else 1

    total_files += len(files)

    if len(commit.modified_files) > 0:
        dmm = (unit_size + complexity + interfacing) / 3
        total_dmm += dmm

avg_files = total_files / total_commits if total_commits else 0
avg_dmm = total_dmm / total_commits if total_commits else 0

output = f"""
Total commits analyzed: {total_commits}
Average number of files changed: {avg_files:.2f}
Average DMM metrics: {avg_dmm:.2f}
"""

print(output)

with open("results.txt", "w") as f:
    f.write(output)