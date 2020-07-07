import typer
import git_speed
from git_speed import installer


app = typer.Typer()


def success(msg: str):
    typer.secho(msg, fg=typer.colors.GREEN, bold=True)


def info(msg: str):
    typer.echo(msg)


def error(msg: str):
    typer.secho(msg, fg=typer.colors.RED, bold=True)
    raise typer.Exit(1)


@app.command()
def install():
    installer.install()
    success("Install Success.")
    info("Run `source ~/.bashrc` or restart Bash to use your new Git aliases.")


@app.command()
def uninstall():
    installer.uninstall()
    success("Uninstall Success.")
    info("Run `source ~/.bashrc` or restart Bash for the changes to take effect.")


@app.callback()
def version_callback(value: bool):
    if value:
        version()


@app.command(hidden=True)
def version():
    typer.echo(f"git-speed version: {git_speed.__version__}")
    raise typer.Exit()


@app.callback()
def options(version: bool = typer.Option(None, "--version", callback=version_callback)):
    """
    git-speed installs Git aliases to help you use Git faster.

    See https://www.gitscientist.com for more.
    """


def main():
    app()
