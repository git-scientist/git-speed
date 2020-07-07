import os
import typer
import shutil
import pathlib

from git_speed import cli

HOME = str(pathlib.Path.home())
ALIAS_INSTALL_PATH = HOME + "/.git_aliases"
BASHRC = HOME + "/.bashrc"
START = "# Managed by git-speed: start"
END = "# Managed by git-speed: end"


def install():
    with open(BASHRC, "r") as f:
        for line in f:
            if START in line:
                reinstall = typer.confirm(
                    "git-speed is already installed. Do you want to reinstall it?"
                )
                if not reinstall:
                    cli.info("Not reinstalling.")
                    raise typer.Abort()
                uninstall()

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
{START}
# See https://pypi.org/project/git-speed/ for more information.
"""
        )

    with open(BASHRC, "a") as f:
        f.write(
            r"""
if [ -f ~/.git_aliases ]; then
    . ~/.git_aliases
fi
"""
        )

    cli.success("Installed aliases.")

    install_prompt = typer.confirm(
        "Would you like to add your current Git branch to your Bash prompt?",
        default=True,
    )

    if install_prompt:
        with open(BASHRC, "a") as f:
            f.write(
                r"""
if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
else
    color_prompt=
fi

parse_git_dirty() {
    [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit"* ]] && echo "~"
}

parse_git_branch() {
    git rev-parse --abbrev-ref HEAD 2> /dev/null | sed "s/\(.*\)/(\1$(parse_git_dirty))/"
}

if [ "$color_prompt" = yes ]; then
    user_style='01;32m'
    dir_style='01;34m'
    git_style='01;33m'
    term_char='$'
    PS1="${debian_chroot:+($debian_chroot)}\[\033[$user_style\]\u@\h\[\033[00m\]:\[\\033[$dir_style\]\w\[\033[$git_style\]\$(parse_git_branch)\[\033[00m\]"$'\n'"$term_char "
else
    PS1="${debian_chroot:+($debian_chroot)}\u@\h:\w\$(parse_git_branch)"$'\n'"\$ "
fi
unset color_prompt
"""
            )

    with open(BASHRC, "a") as f:
        f.write(
            f"""
{END}
"""
        )
        cli.success("Updated Bash prompt.")


def uninstall():
    os.remove(ALIAS_INSTALL_PATH)
    cli.info(f"Deleted {ALIAS_INSTALL_PATH}.")

    out = []
    with open(BASHRC, "r") as f:
        lines = f.readlines()

    append = True
    for line in lines:
        if START in line:
            append = False
            if out[-1] == "\n":
                out = out[:-1]
        if append:
            out.append(line)
        if END in line:
            append = True

    with open(BASHRC, "w") as f:
        f.writelines(out)

    cli.info("Removed git-speed from your .bashrc.")
