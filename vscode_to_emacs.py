#!/bin/env python3

import argparse
import json

class DictNoExcept:
    def __init__(self, d):
        self.d = d
    
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        return None

def write_face(f, name, fg, bg):
    f.write('\t`(%s ((t' % name)
    if fg is not None:
        f.write(' :foreground "%s"' % fg)
    if bg is not None:
        f.write(' :background "%s"' % bg)
    f.write(')))\n')

def write_setting(f, setting):
    sc_to_face = {
        'comment' : 'font-lock-comment-face',
        'string.quoted' : 'font-lock-string-face',
        'variable' : 'font-lock-variable-face',
        'constant' : 'font-lock-constant-face',
        'entity.name.type' : 'font-lock-type-face',
        'entity.name.function' : 'font-lock-function-name-face',
        'keyword' : 'font-lock-keyword-face'
    }

    if type(setting['scope']) is list:
        for scope in setting['scope']:
            if scope in sc_to_face:
                d = DictNoExcept(setting['settings'])
                write_face(f, sc_to_face[scope], d['foreground'], d['background'])
    elif type(setting['scope']) is str:
        scope = setting['scope']
        if scope in sc_to_face:
            d = DictNoExcept(setting['settings'])
            write_face(f, sc_to_face[scope], d['foreground'], d['background'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('vsc', type=str, help='VSCode Theme File')
    args = parser.parse_args()
    og_theme_name = args.vsc.split('.')[0]
    emacs_theme_name = 'emacs-' + og_theme_name
    while emacs_theme_name.endswith('-theme'):
        emacs_theme_name = emacs_theme_name[:-len('-theme')]
    with open(args.vsc, 'r') as f:
        theme = json.load(f)
    
    with open(emacs_theme_name + '-theme.el', 'w') as f:
        f.write('(deftheme %s "Autogenerated port of %s from VS Code to Emacs")\n' % (emacs_theme_name, og_theme_name))
        f.write("(custom-theme-set-faces '%s\n" % emacs_theme_name)
        cols = DictNoExcept(theme['colors'])
        write_face(f, 'default', cols['editor.foreground'], cols['editor.background'])
        write_face(f, 'cursor', cols['editorCursor.foreground'], cols['editorCursor.background'])

        for setting in theme['tokenColors']:
            write_setting(f, setting)
        
        f.write(')\n')
        f.write("\n(provide-theme '%s)\n" % emacs_theme_name)
        

if __name__ == '__main__':
    main()
