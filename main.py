import typer
from typing import Optional
from utils.bookManager import *

app = typer.Typer()


@app.command(name="import")
def import_cmd(
        dir: Optional[str] = typer.Option(None, "-d", "--dir", help="import from Directory, Only PDF"),
        file: Optional[str] = typer.Option(None, "-f", "--file", help="import from File, Only PDF"),
        tag: Optional[str] = typer.Option(None, "-t", "--tag", help="set tag"),
):
    provided_options = [opt for opt in [dir, file] if opt is not None]
    if len(provided_options) != 1:
        typer.echo("error：An option must be specified (--dir/-d or --file/-f)")
        raise typer.Exit(code=1)

    if not tag:
        typer.echo(f"error: no tag specified")
        raise typer.Exit(code=1)

    if dir:
        import_folder(dir, tag)
        typer.echo(f"successfully imported {dir} with {tag}")
    else:
        import_file(file, tag)
        typer.echo(f"successfully imported {file} with {tag}")


@app.command(name="open")
def open_cmd(
        name: Optional[str] = typer.Option(None, "-n", "--name", help="open by book name"),
        id: Optional[int] = typer.Option(None, "-i", "--id", help="open by book ID"),
):
    provided_options = [opt for opt in [name, id] if opt is not None]
    if len(provided_options) != 1:
        typer.echo("error：An option must be specified (--name/-n or --id/-i)")
        raise typer.Exit(code=1)

    if name:
        open_book_by_name(name)
        typer.echo(f"打开书名包含 '{name}' 的书籍")
    elif id:
        open_book_by_id(id)
        typer.echo(f"打开ID为 {id} 的书籍")

@app.command(name="modify")
def modify_cmd(
        name: Optional[str] = typer.Option(..., "-n", "--name", help="modify book name"),
        tag: Optional[str] = typer.Option(..., "-t", "--tag", help="set new tag"),
):
    modify_tag(name,tag)

@app.command(name="archive")
def archive_cmd(
        name: Optional[str] = typer.Option(..., "-n", "--name", help="archive book name")
):
    archive_book(name)

@app.command(name="unarchive")
def unarchive_cmd(
        list:Optional[str] = typer.Option(None  , "-l", "--list", help="list all archived books"),
        name: Optional[str] = typer.Option(None, "-n", "--name", help="unarchive book name"),
):
    provided_options = [opt for opt in [list, name] if opt is not None]
    if len(provided_options) != 1:
        typer.echo("error：An option must be specified (--list/-l or --name/-n)")
        raise typer.Exit(code=1)

    if list:
        list_all_unarchived_books()

    elif name:
        unarchive_book(name)

@app.command(name="remove")
def remove_cmd(
        name: Optional[str] = typer.Option(None, "-n", "--name", help="remove book name"),
        id: Optional[int] = typer.Option(None, "-i", "--id", help="remove book ID"),
):
    provided_options = [opt for opt in [list, name] if opt is not None]
    if len(provided_options) != 1:
        typer.echo("error：An option must be specified (--id/-i or --name/-n)")
        raise typer.Exit(code=1)

    if name:
        remove_book_by_name(name)
    elif id:
        remove_book_by_id(id)

@app.command(name="list")
def list_cmd(
        tag: Optional[str] = typer.Option(None, "-t", "--tag", help="list books of tag"),
):
    if tag is None:
        list_tags()
    else:
        list_books(tag)

@app.command(name="export")
def export_cmd(
        tag: str = typer.Option(..., "-t", "--tag", help="export books of tag"),
        dir: str = typer.Option(..., "-d", "--dir", help="output directory")
):
    pass


if __name__ == "__main__":
    app()
