# -*- coding: utf-8 -*-
import maya.mel as mel
import maya.cmds as cmds
import maya.utils

thickness = 0
thicknessMultiplay = 0.2
ThicknessField = None


def AppWindow():
    if cmds.window('EdgeToPoly', ex=1):
        cmds.deleteUI('EdgeToPoly')
    windowName = cmds.window('EdgeToPoly', title='EdgeToPoly')

    tabTest = cmds.tabLayout(
        scrollable=False, innerMarginHeight=5, innerMarginWidth=1)
    hoge = cmds.columnLayout(adj=True, rowSpacing=10)
    cmds.rowLayout(numberOfColumns=4, columnAttach4=(
        'left', 'left', 'left', 'left'), columnWidth4=(100, 150, 150, 150))
    cmds.text(label="Thickness")
    ThicknessField = cmds.floatField("myIntField", minValue=0, maxValue=1, width=60,
                                     changeCommand="OnButtonClick()")
    cmds.showWindow()


def OnButtonClick():
    # Init
    name = ""
    sel_ID = None
    thickness = cmds.floatField("myIntField", q=True, v=True)

    cmds.polyTriangulate()

    cmds.polyBevel3(f=thickness, oaf=True, sn=True, sg=1, d=1,
                    mvt=0.0001, ws=True, sa=40, ch=0, mv=False, ma=180, c=False)
    #Just in case
    maya.utils.processIdleEvents()

    # Select 4Face
    mel.eval('CleanupPolygon')
    mel.eval('performPolyCleanup 0')

    # Get Name
    mel.eval("changeSelectMode -object")
    sel_ID = cmds.ls(sl=True, uuid=True)[0]
    name = cmds.ls(sel_ID)[0]
    mel.eval("changeSelectMode -component")

    # Invert Select
    cmds.select(name+".f[*]", tgl=True)
    cmds.delete()
    # All Select
    cmds.select(name+".f[*]")

    cmds.polyExtrudeFacet(tk=thickness*thicknessMultiplay)


if __name__ == '__main__':
    AppWindow()