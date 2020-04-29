import os
import typer
import shutil
import pathlib

from git_speed import cli

HOME = str(pathlib.Path.home())
ALIAS_INSTALL_PATH = HOME + "/.git_aliases"
BASHRC = HOME + "/.bashrc"


def install():
    if os.path.exists(ALIAS_INSTALL_PATH):
        delete = typer.confirm(
            f"{ALIAS_INSTALL_PATH} already exists. Do you want to delete it?"
        )
        if not delete:
            cli.info("Not deleting.")
            raise typer.Abort()
        os.remove(ALIAS_INSTALL_PATH)

    alias_dir = os.path.dirname(os.path.abspath(__file__))
    cli.info(f"Installing Git aliases to {ALIAS_INSTALL_PATH}")
    shutil.copyfile(alias_dir + "/git_aliases", ALIAS_INSTALL_PATH)

    with open(BASHRC, "a") as f:
        f.write(
            f"""
# Added by git-speed
if [ -f {ALIAS_INSTALL_PATH} ]; then
    . {ALIAS_INSTALL_PATH}
fi
"""
        )
