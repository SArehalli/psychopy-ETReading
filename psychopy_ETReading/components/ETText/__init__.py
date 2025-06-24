#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2025 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

from pathlib import Path
from psychopy.alerts import alerttools
from psychopy.experiment.components import BaseVisualComponent, Param, getInitVals, _translate


class ETTextComponent(BaseVisualComponent):
    """An event class for presenting text-based stimuli for Eyetracking-While-Reading paradigms with word-by-word regions
    """

    categories = ['Stimuli']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'example.png'
    tooltip = _translate('ETText: present text stimuli for word-level ROI eyetracking.')

    def __init__(self, exp, parentName, name='text',
                 # effectively just a display-value
                 text=_translate('Any text\n\nincluding line breaks'),
                 font='Arial', units='from exp settings',
                 color='white', colorSpace='rgb',
                 pos=(0, 0), letterHeight=0.05,
                 ori=0, draggable=False,
                 startType='time (s)', startVal=0.0,
                 stopType='duration (s)', stopVal=1.0,
                 flip='None', startEstim='', durationEstim='', wrapWidth='',
                 languageStyle='LTR', padWidth=0.05, align="left", debug=False):
        super(ETTextComponent, self).__init__(exp, parentName, name=name,
                                            units=units,
                                            color=color,
                                            colorSpace=colorSpace,
                                            pos=pos,
                                            ori=ori,
                                            startType=startType,
                                            startVal=startVal,
                                            stopType=stopType,
                                            stopVal=stopVal,
                                            startEstim=startEstim,
                                            durationEstim=durationEstim)
        self.type = 'ETText'
        self.url = ""

        # params
        _allow3 = ['constant', 'set every repeat', 'set every frame']  # list
        self.params['text'] = Param(
            text, valType='str', inputType="multi", allowedTypes=[], categ='Basic',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=_translate("The text to be displayed"),
            canBePath=False,
            label=_translate("Text"))
        self.params['font'] = Param(
            font, valType='str', inputType="font", allowedTypes=[], categ='Formatting',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=_translate("The font name (e.g. Comic Sans)"),
            label=_translate("Font"))
        del self.params['size']  # because you can't specify width for text
        self.params['letterHeight'] = Param(
            letterHeight, valType='num', inputType="single", allowedTypes=[], categ='Formatting',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=_translate("Specifies the height of the letter (the width"
                            " is then determined by the font)"),
            label=_translate("Letter height"))

        self.params['padWidth'] = Param(
            padWidth, valType='num', inputType="single", allowedTypes=[], categ='Formatting',
            updates='constant', allowedUpdates=_allow3[:],  # copy the list
            hint=_translate("Space between words (i.e., width of the space character)"),
            label=_translate("Word Padding Width"))

        self.params['wrapWidth'] = Param(
            wrapWidth, valType='num', inputType="single", allowedTypes=[], categ='Layout',
            updates='constant', allowedUpdates=['constant'],
            hint=_translate("How wide should the text get when it wraps? (in"
                            " the specified units)"),
            label=_translate("Wrap width"))

        self.params['align'] = Param(
            align, valType='str', inputType="choice", categ='Formatting',
            allowedVals=['left', 'right'],
            hint=_translate("Alignment/Anchoring for the text object. For now, only left is supported..."),
            label=_translate("Alignment/Anchoring"))

        self.params['languageStyle'] = Param(
            languageStyle, valType='str', inputType="choice", categ='Formatting',
            allowedVals=['LTR', 'RTL', 'Arabic'],
            hint=_translate("Handle right-to-left (RTL) languages and Arabic reshaping"),
            label=_translate("Language style"))

        self.params['debug'] = Param(
            debug, valType='bool', inputType="bool", categ='Formatting',
            allowedVals=[],
            hint=_translate("Display bounding boxes for regions"),
            label=_translate("Debug Bounding Boxes"))

        del self.params['fillColor']
        del self.params['borderColor']

    def _getParamCaps(self, paramName):
        """
        TEMPORARY FIX

        TextStim in JS doesn't accept `letterHeight` as a param. Ideally this needs to be fixed
        in JS, but in the meantime overloading this function in Python to write `setHeight`
        rather than `setLetterHeight` means it stops biting users.
        """
        # call base function
        paramName = BaseVisualComponent._getParamCaps(self, paramName)
        # replace letterHeight
        if paramName == "LetterHeight":
            paramName = "Height"

        return paramName

    def writeInitCode(self, buff):
        # do we need units code?
        if self.params['units'].val == 'from exp settings':
            unitsStr = ""
        else:
            unitsStr = "units=%(units)s, " % self.params
        # do writing of init
        # replaces variable params with sensible defaults
        inits = getInitVals(self.params, 'PsychoPy')
        if self.params['wrapWidth'].val in ['', 'None', 'none']:
            inits['wrapWidth'] = 'None'

        code =  ("words = {text}.split()\n"
                 "pad = {padWidth}\n"
                 "cur_pos = {pos}\n\n"
                 "class WordList:\n"
                 "    words = []\n"
                 "    status = None\n"
                 "{name} = WordList()\n\n"
                 "for word in words:\n"
                 "    word_{name} = visual.TextStim(win=win, name='{name}',\n"
                 "        text=word,\n"
                 "        font={font},\n"
                 "        pos=cur_pos, draggable=False, height={letterHeight}, wrapWidth=None, ori={ori}, \n"
                 "        color={color}, colorSpace={colorSpace}, opacity={opacity}, \n"
                 "        anchorHoriz={align}, alignHoriz={align},\n"
                 "        languageStyle={languageStyle},\n"
                 "        depth={depth:.1f});\n"
                 "    {name}.words.append(word_{name})\n"
                 "    cur_pos = (cur_pos[0] + word_{name}.boundingBox[0] + pad, cur_pos[1])\n"
                 "    x, y = word_{name}.posPix\n"
                 "    dx, dy = word_{name}.boundingBox\n"
                 "    wordroi = (x, y + dy//2, x + dx + pad, y - dy//2)\n"
                 "    {currentloop}.addData('{name}.' + word + '.loc', wordroi)\n" 
                 "    print(word, wordroi)\n")
        inits["depth"] = -self.getPosInRoutine()
        inits["currentloop"] = self.currentLoop
        if self.params["debug"]:
            debug_code = ("    box_{name} = visual.Rect(win=win, name='{name}',\n"
                          "        pos = (x, y + dy//2), size=(dx + pad, dy),\n"
                          "        lineColor='red', fillColor=None, anchor='top-left')\n"
                          "    {name}.words.append(box_{name})\n")
            code += debug_code
        buff.writeIndentedLines(code.format(**inits))

    def writeFrameCode(self, buff):
        """
        Write the Python code which is called each frame for this Component.

        Parameters
        ----------
        buff : 
            String buffer to write to, i.e. the .py file
        """

        # update any parameters which need updating
        self.writeParamUpdates(buff, updateType="set every frame")

        dedent = self.writeStartTestCode(buff)
        # we only want the following code written if an if loop actually was opened, not if the start time is None! so make sure to use dedent as a boolean to avoid writing broken code
        if dedent:
            # dedent after!
            code = (
                "for word in {name}.words:\n"
                "    word.autoDraw = True\n"
            )
            buff.writeIndentedLines(code.format(**self.params))
            buff.setIndentLevel(-dedent, relative=True)
