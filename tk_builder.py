import tkinter as tk
import tkinter.ttk as ttk
import cssutils
import os
import re

css_parser = cssutils.CSSParser()
dir_filenames = os.listdir("styles")
sheets: list[cssutils.css.CSSStyleSheet] = []
style = ttk.Style()

default_style = ".layer-1 .normal"
def default(style: str):
    default_style = style

for filename in dir_filenames:
    if filename.endswith(".css"):
        sheets.append(css_parser.parseFile("styles/" + filename))

for sheet in sheets:
    for rule in sheet.cssRules:
        for key in rule.style.keys():
            match key:
                case "background-color":
                    style.configure(rule.selectorText, background=rule.style[key])
                case "font":
                    font_configs = rule.style[key].split()
                    result_configs = []
                    for config in font_configs:
                        font_styles = ["bold", "italic", "normal", "roman"]
                        if config in font_styles:
                            result_configs[2] = config
                        elif re.match(r"$[1-9][0-9]*pt^", config):
                            result_configs[1] = config[:-2]
                        else:
                            result_configs[0] = config
                    style.configure(rule.selectorText, font=tuple(result_configs))
                case _:
                    style.configure(rule.selectorText, {key: rule.style[key]})

def get(what: str, master: tk.Misc | None = None, style: str = default_style):
    result = None
    
    match what.lower():
        case "tk":
            result = tk.Tk()
        case "frame":
            result = tk.Frame(master)
        case "label":
            result = tk.Label(master)
        case "entry":
            result = tk.Entry(master)
        case "button":
            result = tk.Button(master)

    