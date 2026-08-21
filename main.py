import customtkinter as ctk
from json import load, dump, JSONDecodeError
from os.path import exists, join, expanduser
from os import mkdir

color = "#5D6658"
dark_color = "#50594C"

PATH = join(expanduser("~"), "litter")
if not exists(PATH):
    mkdir(PATH)

BOOKS_PATH = join(PATH, "books.json")
if not exists(BOOKS_PATH):
    with open(BOOKS_PATH, "w", encoding="utf-8") as f:
        dump({}, f, indent=4)

SETTINGS_PATH = join(PATH, "settings.json")
if not exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        dump({"main_color": color, "dark_color": dark_color}, f, indent=4)

with open(BOOKS_PATH, "r") as f:
    books_json = load(f)

with open(SETTINGS_PATH, "r") as f:
    set_json = load(f)

def refresh():
    for widget in b_frame.winfo_children():
        widget.destroy()
    for k, v in books_json.items():
        but = ctk.CTkButton(
            master=b_frame,
            text=k,
            corner_radius=0,
            font=app_font,
            fg_color=ucolor,
            bg_color="transparent",
            hover_color=dark_ucolor,
            command=lambda t=k, au=v['author'], p=v['pages'], ab=v['about']: get_info(t,au,p,ab)
        )
        but.pack(fill="x", padx=0)

def new_book():
    def confirm():
        try:
            if title.get().strip():
                with open(BOOKS_PATH, "w") as f:
                    books_json[title.get()] = {
                        "author": new_author.get(),
                        "pages": new_pages.get(),
                        "about": new_about.get()
                    }
                    dump(books_json, f, indent=4)
            refresh()
            new.destroy()
        except KeyError:
            with open(BOOKS_PATH, "w") as f:
                dump(books_json, f, indent=4)

    def cancel():
        new.destroy()

    new = ctk.CTkToplevel()
    new.title("New/Configure Book")
    if exists(join(PATH, "litter.ico")):
        new.iconbitmap(join(PATH, "litter.ico"))
    new.resizable(False, False)
    new.geometry("400x260")

    title = ctk.CTkEntry(
        master=new,
        corner_radius=0,
        placeholder_text="Title to add/change...",
        font=app_font
    )
    title.pack(fill="x", pady=10, padx=10)

    new_author = ctk.CTkEntry(
        master=new,
        corner_radius=0,
        placeholder_text="Author...",
        font=app_font
    )
    new_author.pack(fill="x", pady=10, padx=10)

    new_pages = ctk.CTkEntry(
        master=new,
        corner_radius=0,
        placeholder_text="Number of pages...",
        font=app_font
    )
    new_pages.pack(fill="x", pady=10, padx=10)

    new_about = ctk.CTkEntry(
        master=new,
        corner_radius=0,
        placeholder_text="About the book...",
        font=app_font
    )
    new_about.pack(fill="x", pady=10, padx=10)

    drop_actions = ctk.CTkFrame(
        master=new
    )
    drop_actions.pack(side="bottom", fill="x", expand=True, padx=10)

    ok = ctk.CTkButton(
        master=drop_actions,
        text="OK",
        fg_color=ucolor,
        hover_color=dark_ucolor,
        font=app_font,
        corner_radius=0,
        command=confirm
    )
    ok.pack(side="left",fill="x",expand=True, padx=1, pady=0)

    no = ctk.CTkButton(
        master=drop_actions,
        text="Cancel",
        fg_color=ucolor,
        hover_color=dark_ucolor,
        font=app_font,
        command=cancel,
        corner_radius=0
    )
    no.pack(side="left",fill="x",expand=True, padx=1, pady=0)

    for widget in b_frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") not in books_json.keys():
            widget.destroy()

def delete_book():
    try:
        def confirm():
            try:
                if title.get().strip():
                    with open(BOOKS_PATH, "w") as f:
                        books_json.pop(title.get())
                        dump(books_json, f, indent=4)
                for widget in b_frame.winfo_children():
                    if widget.cget("text") not in books_json.keys():
                        widget.destroy()
                new.destroy()
            except KeyError:
                with open(BOOKS_PATH, "w") as f:
                    dump(books_json, f, indent=4)

        def cancel():
            new.destroy()

        new = ctk.CTkToplevel()
        new.title("Drop Book")
        new.resizable(False, False)
        new.geometry("400x80")
        if exists(join(PATH, "litter.ico")):
            new.iconbitmap(join(PATH, "litter.ico"))

        title = ctk.CTkEntry(
            master=new,
            corner_radius=0,
            placeholder_text="Title to delete...",
            font=app_font
        )
        title.pack(fill="x", pady=10, padx=10)

        drop_actions = ctk.CTkFrame(
            master=new
        )
        drop_actions.pack(side="bottom", fill="x", expand=True, padx=10)

        ok = ctk.CTkButton(
            master=drop_actions,
            text="OK",
            fg_color=ucolor,
            hover_color=dark_ucolor,
            font=app_font,
            corner_radius=0,
            command=confirm
        )
        ok.pack(side="left",fill="x",expand=True, padx=1, pady=0)

        no = ctk.CTkButton(
            master=drop_actions,
            text="Cancel",
            fg_color=ucolor,
            hover_color=dark_ucolor,
            font=app_font,
            command=cancel,
            corner_radius=0
        )
        no.pack(side="left",fill="x",expand=True, padx=1, pady=0)
    except (JSONDecodeError, FileNotFoundError):
        with open(BOOKS_PATH, "w") as f:
            dump({}, f, indent=4)

    for widget in b_frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") not in books_json.keys():
            widget.destroy()

def get_info(title, author, pages, about):
    name.configure(text=title)
    name.pack()
    auth.configure(text=f"Author: {author}")
    auth.pack()
    pag.configure(text=f"Page count: {pages}")
    pag.pack()
    info.configure(text=f"{about}")
    info.pack()

def update_buttons(frame: ctk.CTkFrame | ctk.CTkScrollableFrame, c, dc):
    for widget in frame.winfo_children():
        if isinstance(widget, ctk.CTkButton):
            widget.configure(fg_color=c, hover_color=dc)

def is_color(string: str):
    chars_check = set([x.isnumeric() for x in string])==set([True])
    if len(string) == 6 and chars_check:
        return True
    if not string or len(string)!=7:
        return False
    if string[0] != "#" or chars_check:
        return False
    return True

def apply_changes():
    if is_color(ucolor_prompt.get()) and is_color(hover_prompt.get()):
        global ucolor, dark_ucolor
        ucolor = f"#{ucolor_prompt.get().removeprefix('#')}"
        dark_ucolor = f"#{hover_prompt.get().removeprefix('#')}"
        tabs.configure(
            segmented_button_selected_color=ucolor,
            segmented_button_selected_hover_color=dark_ucolor
        )

        update_buttons(b_frame, ucolor, dark_ucolor)
        update_buttons(action_frame, ucolor, dark_ucolor)
        update_buttons(settings_actions, ucolor, dark_ucolor)

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        dump({"main_color": ucolor, "dark_color": dark_ucolor}, f, indent=4)

def revert_changes():
    global ucolor, dark_ucolor
    ucolor = color
    dark_ucolor = dark_color
    tabs.configure(
        segmented_button_selected_color=color,
        segmented_button_selected_hover_color=dark_color
    )

    update_buttons(b_frame, color, dark_color)
    update_buttons(action_frame, color, dark_color)
    update_buttons(settings_actions, color, dark_color)

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        dump({"main_color": ucolor, "dark_color": dark_ucolor}, f, indent=4)

root = ctk.CTk()
root.geometry("800x470")
root.title("Litter")
root.minsize(600,300)

if exists(join(PATH, "litter.ico")):
    root.iconbitmap(join(PATH, "litter.ico"))

app_font = ("Inter", 16)
s_app_font = ("Inter", 14)
ucolor = set_json["main_color"]
dark_ucolor = set_json["dark_color"]

panel = ctk.CTkFrame(root, corner_radius=0)
panel.pack(side="left", fill="y", padx=0)

tabs = ctk.CTkTabview(
    panel, 
    segmented_button_font=s_app_font,
    segmented_button_selected_color=ucolor,
    segmented_button_selected_hover_color=dark_ucolor,
    corner_radius=4
)
tabs.add("Books")
tabs.add("Settings")
tabs.pack(side="left", fill="y", pady=(0,10), padx=10)
b_frame = ctk.CTkScrollableFrame(
    master=tabs.tab("Books"),
    height=30,
    corner_radius=0,
    fg_color="transparent",
)
b_frame.pack(fill="both",expand=True,pady=(0,5),padx=0)

refresh()

action_frame = ctk.CTkFrame(
    master=tabs.tab("Books"),
    height=30,
    width=90,
    fg_color="transparent",
)
action_frame.pack(side="bottom", fill="x")

drop_book = ctk.CTkButton(
    master=action_frame,
    text="Drop",
    font=app_font,
    fg_color=ucolor,
    hover_color=dark_ucolor,
    corner_radius=0,
    command=delete_book,
    bg_color="transparent"
)
drop_book.pack(fill="x", side="left", expand=True)

add_book = ctk.CTkButton(
    master=action_frame,
    text="Add",
    font=app_font,
    fg_color=ucolor,
    hover_color=dark_ucolor,
    corner_radius=0,
    command=new_book,
    bg_color="transparent"
)
add_book.pack(fill="x", side="left", expand=True)

info_frame = ctk.CTkFrame(
    master=root,
    corner_radius=0,
    fg_color="transparent"
)
info_frame.pack(fill="x", expand=True)

name = ctk.CTkLabel(
    master=info_frame,
    text="",
    font=(app_font[0], 33)
)
name.pack(pady=(10, 1))

auth = ctk.CTkLabel(
    master=info_frame,
    text="",
    font=app_font
)
auth.pack(pady=1)

pag = ctk.CTkLabel(
    master=info_frame,
    text="",
    font=app_font
)
pag.pack(pady=1)

info = ctk.CTkLabel(
    master=info_frame,
    text="",
    font=app_font
)
info.pack(pady=(1, 10))

ucolor_prompt = ctk.CTkEntry(
    master=tabs.tab("Settings"),
    placeholder_text="Enter color...",
    font=app_font,
    corner_radius=0
)
ucolor_prompt.pack(fill="x",pady=2)

hover_prompt = ctk.CTkEntry(
    master=tabs.tab("Settings"),
    placeholder_text="Enter hover color...",
    font=app_font,
    corner_radius=0
)
hover_prompt.pack(fill="x",pady=2)

settings_actions = ctk.CTkFrame(tabs.tab("Settings"), fg_color="transparent")
settings_actions.pack(side="bottom", fill="x", pady=0)

confirm_settings = ctk.CTkButton(
    master=settings_actions,
    font=app_font,
    text="OK",
    fg_color=ucolor,
    hover_color=dark_ucolor,
    corner_radius=0,
    command=apply_changes
)
confirm_settings.pack(side="left", fill="x" ,pady=0, expand=True)

revert_settings = ctk.CTkButton(
    master=settings_actions,
    font=app_font,
    text="Revert Changes",
    fg_color=ucolor,
    hover_color=dark_ucolor,
    corner_radius=0,
    command=revert_changes
)
revert_settings.pack(side="left", fill="x" ,pady=0, expand=True)

root.mainloop()