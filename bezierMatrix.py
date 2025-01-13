'''
bezierMatrix.py

author:         Thibaut Massart

description:    Tool for creating Bezier behavior with matrix nodes and a pinch attribute on each Bezier controller.

usage:
                1 - Copy bezierMatrix.py in your maya script folder

                2 - Select your bezier controllers

                3 - Run this code :

                import bezierMatrix
                bezierMatrix.mainProc()
'''

import maya.cmds as cmds
import maya.mel as mel


def mainProc():
    bezierCtrls = getBezierControllers()
    if bezierCtrls:
        floatConstantZeroName = setFloatConstantZero()
        floatConstantOneName = setFloatConstantOne()

        rootName = setRoot()
        setPinchAttributes(bezierCtrls)
        bezierPinchLocators = setBezierPinchLocators(bezierCtrls=bezierCtrls, floatConstantZeroName=floatConstantZeroName, floatConstantOneName=floatConstantOneName, rootName=rootName)
        newBezierHandleNames = setNewBezierHandleNames(pinchHandleNames=bezierPinchLocators)
        bezierSkinJointNames = setBezierSkinJoints(newBezierHandleNames=newBezierHandleNames, rootName=rootName)

    else:
        cmds.warning('Select some objects, in order to make them bezier controllers')


def setRoot():
    rootName = 'bezierRoot'
    cmds.group(em=1, n=rootName)
    return rootName


def getBezierControllers():
    bezierCtrls = cmds.ls(os=True)
    return bezierCtrls


def setFloatConstantZero():
    floatConstantZeroName = setDigit('floatConstantZero')
    cmds.createNode('floatConstant', n=floatConstantZeroName)
    cmds.setAttr(floatConstantZeroName + '.inFloat', 0)
    return floatConstantZeroName


def setFloatConstantOne():
    floatConstantOneName = setDigit('floatConstantOne')
    cmds.createNode('floatConstant', n=floatConstantOneName)
    cmds.setAttr(floatConstantOneName + '.inFloat', 1)
    return floatConstantOneName


def setPinchAttributes(bezierCtrls):
    pinchAttributeInName = 'pinch'
    blendValue = 0.5
    for bezierHandleName in bezierCtrls:
        cmds.addAttr(bezierHandleName, longName=pinchAttributeInName, attributeType="float", defaultValue=blendValue, k=True)


def setBezierPinchLocators(bezierCtrls, floatConstantZeroName, floatConstantOneName, rootName):
    bezierPinchLocatorsRootName = 'bezierPinchLocatorsRoot'
    cmds.group(em=1, n=bezierPinchLocatorsRootName)
    cmds.parent(bezierPinchLocatorsRootName, rootName)
    cmds.setAttr(bezierPinchLocatorsRootName + '.visibility', 0)

    bezierPinchHandleNames = {}
    for i in range(len(bezierCtrls)):

        if i == 0:
            bezierPinchNames = []
            bezierBlendMtxName = setDigit(bezierCtrls[i] + 'InterBlendMtx')
            cmds.createNode('blendMatrix', n=bezierBlendMtxName)

            bezierLocName = setDigit(bezierCtrls[i] + 'Pinch')
            bezierPinchNames.append(bezierLocName)
            cmds.spaceLocator(n=bezierLocName)
            cmds.setAttr(bezierLocName + '.overrideEnabled', 1)
            cmds.setAttr(bezierLocName + '.overrideColor', 17)
            cmds.parent(bezierLocName, bezierPinchLocatorsRootName)

            cmds.connectAttr(bezierCtrls[i] + '.worldMatrix[0]', bezierBlendMtxName + '.inputMatrix')
            cmds.connectAttr(bezierCtrls[i + 1] + '.worldMatrix[0]', bezierBlendMtxName + '.target[0].targetMatrix')
            setPinchBlendWeight(bezierCtrls[i], floatConstantZeroName, floatConstantOneName, bezierBlendMtxName)

            cmds.connectAttr(bezierBlendMtxName + '.outputMatrix', bezierLocName + '.offsetParentMatrix')

            bezierPinchHandleNames[bezierCtrls[i]] = bezierPinchNames


        elif i == range(len(bezierCtrls))[-1]:
            bezierPinchNames = []
            bezierBlendMtxName = setDigit(bezierCtrls[i] + 'InterBlendMtx')
            cmds.createNode('blendMatrix', n=bezierBlendMtxName)

            bezierLocName = setDigit(bezierCtrls[i] + 'Pinch')
            bezierPinchNames.append(bezierLocName)
            cmds.spaceLocator(n=bezierLocName)
            cmds.setAttr(bezierLocName + '.overrideEnabled', 1)
            cmds.setAttr(bezierLocName + '.overrideColor', 17)
            cmds.parent(bezierLocName, bezierPinchLocatorsRootName)

            cmds.connectAttr(bezierCtrls[i] + '.worldMatrix[0]', bezierBlendMtxName + '.inputMatrix')
            cmds.connectAttr(bezierCtrls[i - 1] + '.worldMatrix[0]', bezierBlendMtxName + '.target[0].targetMatrix')
            setPinchBlendWeight(bezierCtrls[i], floatConstantZeroName, floatConstantOneName, bezierBlendMtxName)

            cmds.connectAttr(bezierBlendMtxName + '.outputMatrix', bezierLocName + '.offsetParentMatrix')

            bezierPinchHandleNames[bezierCtrls[i]] = bezierPinchNames


        else:
            bezierPinchNames = []
            bezierBlendMtxName = setDigit(bezierCtrls[i] + 'InterBlendMtx')
            cmds.createNode('blendMatrix', n=bezierBlendMtxName)

            bezierLocName = setDigit(bezierCtrls[i] + 'Pinch')
            bezierPinchNames.append(bezierLocName)
            cmds.spaceLocator(n=bezierLocName)
            cmds.setAttr(bezierLocName + '.overrideEnabled', 1)
            cmds.setAttr(bezierLocName + '.overrideColor', 17)
            cmds.parent(bezierLocName, bezierPinchLocatorsRootName)

            cmds.connectAttr(bezierCtrls[i] + '.worldMatrix[0]', bezierBlendMtxName + '.inputMatrix')
            cmds.connectAttr(bezierCtrls[i - 1] + '.worldMatrix[0]', bezierBlendMtxName + '.target[0].targetMatrix')
            setPinchBlendWeight(bezierCtrls[i], floatConstantZeroName, floatConstantOneName, bezierBlendMtxName)

            cmds.connectAttr(bezierBlendMtxName + '.outputMatrix', bezierLocName + '.offsetParentMatrix')

            bezierBlendMtxName = setDigit(bezierCtrls[i] + 'InterBlendMtx')
            cmds.createNode('blendMatrix', n=bezierBlendMtxName)

            bezierLocName = setDigit(bezierCtrls[i] + 'Pinch')
            bezierPinchNames.append(bezierLocName)
            aaa = cmds.spaceLocator(n=bezierLocName)
            cmds.setAttr(bezierLocName + '.overrideEnabled', 1)
            cmds.setAttr(bezierLocName + '.overrideColor', 17)
            cmds.parent(bezierLocName, bezierPinchLocatorsRootName)

            cmds.connectAttr(bezierCtrls[i] + '.worldMatrix[0]', bezierBlendMtxName + '.inputMatrix')
            cmds.connectAttr(bezierCtrls[i + 1] + '.worldMatrix[0]', bezierBlendMtxName + '.target[0].targetMatrix')
            setPinchBlendWeight(bezierCtrls[i], floatConstantZeroName, floatConstantOneName, bezierBlendMtxName)

            cmds.connectAttr(bezierBlendMtxName + '.outputMatrix', bezierLocName + '.offsetParentMatrix')
            bezierPinchHandleNames[bezierCtrls[i]] = bezierPinchNames

    return bezierPinchHandleNames


def setPinchBlendWeight(bezierCtrls, floatConstantZeroName, floatConstantOneName, bezierBlendMtxName):
    blendTwoAttrName = setDigit(bezierCtrls + 'BlendTwoAttr')
    cmds.createNode('blendTwoAttr', n=blendTwoAttrName)

    cmds.connectAttr(bezierCtrls + '.pinch', blendTwoAttrName + '.attributesBlender')
    cmds.connectAttr(floatConstantOneName + '.outFloat', blendTwoAttrName + '.input[0]')
    cmds.connectAttr(floatConstantZeroName + '.outFloat', blendTwoAttrName + '.input[1]')
    cmds.connectAttr(blendTwoAttrName + '.output', bezierBlendMtxName + '.target[0].weight')

    return blendTwoAttrName


def setDigit(inputName):
    digit = 1
    while cmds.objExists(inputName + '_' + str(digit)):
        digit += 1
    outputName = inputName + '_' + str(digit)
    return (inputName + '_' + str(digit))


def setNewBezierHandleNames(pinchHandleNames):
    newBezierHandleNames = []
    i = 0
    for bezierHandleName in pinchHandleNames:
        if i == 0:
            newBezierHandleNames.append(bezierHandleName)
            newBezierHandleNames.append(pinchHandleNames[bezierHandleName][0])
        elif i == len(pinchHandleNames) - 1:
            newBezierHandleNames.append(pinchHandleNames[bezierHandleName][0])
            newBezierHandleNames.append(bezierHandleName)
        else:
            newBezierHandleNames.append(pinchHandleNames[bezierHandleName][0])
            newBezierHandleNames.append(bezierHandleName)
            newBezierHandleNames.append(pinchHandleNames[bezierHandleName][1])
        i += 1
    return newBezierHandleNames


def setBezierSkinJoints(newBezierHandleNames, rootName):
    mainProgressBar = mel.eval('$tmp = $gMainProgressBar');

    bezierSkinJointsRootName = 'bezierSkinJointsRoot'
    cmds.group(em=1, n=bezierSkinJointsRootName)
    cmds.parent(bezierSkinJointsRootName, rootName)

    bezierBlendCompMtxNames = []
    skinJointCount = len(newBezierHandleNames)
    bezierJointWeigth = 0

    currentTaskTitle = 'Building bezier matrix'
    cmds.progressBar(mainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status=currentTaskTitle, maxValue=skinJointCount)

    for i in range(skinJointCount):
        bezierBlendCompMtxName = setBezierBlends(newBezierHandleNames, bezierJointWeigth)
        bezierBlendCompMtxNames.append(bezierBlendCompMtxName)
        bezierJointWeigth += 1 / (skinJointCount - 1)

        cmds.progressBar(mainProgressBar, edit=True, step=1)

    cmds.progressBar(mainProgressBar, edit=True, endProgress=True)

    currentTaskTitle = 'Building joints on bezier'
    cmds.progressBar(mainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status=currentTaskTitle, maxValue=len(bezierBlendCompMtxNames))

    bezierSkinJointNames = []
    for bezierBlendCompMtxName in bezierBlendCompMtxNames:
        cmds.select(cl=True)
        bezierSkinJointName = setDigit('bezierSkinJoint')
        cmds.joint(n=bezierSkinJointName)
        cmds.setAttr(bezierSkinJointName + '.overrideEnabled', 1)
        cmds.setAttr(bezierSkinJointName + '.overrideColor', 9)
        cmds.setAttr(bezierSkinJointName + '.displayLocalAxis', 1)
        cmds.setAttr(bezierSkinJointName + '.radius', 0.8)
        cmds.parent(bezierSkinJointName, bezierSkinJointsRootName)

        cmds.connectAttr(bezierBlendCompMtxName + '.outputMatrix', bezierSkinJointName + '.offsetParentMatrix')
        bezierSkinJointNames.append(bezierSkinJointName)

        cmds.progressBar(mainProgressBar, edit=True, step=1)

    bezier4By4MatrixNames = setBezierXOrient(bezierSkinJointNames, bezierBlendCompMtxNames)
    setBezierYOrient(bezierBlendCompMtxNames, bezier4By4MatrixNames)

    cmds.progressBar(mainProgressBar, edit=True, endProgress=True)

    return bezierSkinJointNames


def setBezierBlends(newBezierHandleNames, bezierLocationWeigth=0.5):
    newBezierBlendMtxNames = []
    for i in range(len(newBezierHandleNames) - 1):

        bezierBlendMtxNames = newBezierBlendMtxNames
        if i == 0:
            for i in range(len(newBezierHandleNames) - 1):
                bezierBlendMtxName = setDigit('bezierBlendMtx')
                blendMtx = cmds.createNode('blendMatrix', n=bezierBlendMtxName)

                cmds.connectAttr(newBezierHandleNames[i] + '.worldMatrix[0]', bezierBlendMtxName + '.inputMatrix')
                cmds.connectAttr(newBezierHandleNames[i + 1] + '.worldMatrix[0]', bezierBlendMtxName + '.target[0].targetMatrix')
                cmds.setAttr(bezierBlendMtxName + '.target[0].weight', bezierLocationWeigth)

                bezierBlendMtxNames.append(bezierBlendMtxName)
        else:
            newBezierBlendMtxNames = []
            for i in range(len(bezierBlendMtxNames) - 1):
                bezierBlendMtxName = setDigit('bezierBlendMtx')
                blendMtx = cmds.createNode('blendMatrix', n=bezierBlendMtxName)

                cmds.connectAttr(bezierBlendMtxNames[i] + '.outputMatrix', bezierBlendMtxName + '.inputMatrix')
                cmds.connectAttr(bezierBlendMtxNames[i + 1] + '.outputMatrix', bezierBlendMtxName + '.target[0].targetMatrix')
                cmds.setAttr(bezierBlendMtxName + '.target[0].weight', bezierLocationWeigth)

                newBezierBlendMtxNames.append(bezierBlendMtxName)

        bezierBlendDecompMtxName = setDigit('bezierBlendDecompMtx')
        bezierBlendDecompMtx = cmds.createNode('decomposeMatrix', n=bezierBlendDecompMtxName)
        cmds.connectAttr(bezierBlendMtxName + '.outputMatrix', bezierBlendDecompMtxName + '.inputMatrix')

        bezierBlendCompMtxName = setDigit('bezierBlendCompMtx')
        bezierBlendCompMtx = cmds.createNode('composeMatrix', n=bezierBlendCompMtxName)
        cmds.connectAttr(bezierBlendDecompMtxName + '.outputQuat', bezierBlendCompMtxName + '.inputQuat')
        cmds.connectAttr(bezierBlendDecompMtxName + '.outputScale', bezierBlendCompMtxName + '.inputScale')
        cmds.connectAttr(bezierBlendDecompMtxName + '.outputShear', bezierBlendCompMtxName + '.inputShear')
        cmds.connectAttr(bezierBlendDecompMtxName + '.outputTranslate', bezierBlendCompMtxName + '.inputTranslate')

    return bezierBlendCompMtxName


def setBezierXOrient(bezierSkinLocatorNames, bezierBlendCompMtxNames):
    i = 0
    bezier4By4MatrixNames = []
    for bezierSkinLocatorName in bezierSkinLocatorNames:
        sourceCompMtxName = cmds.listConnections(bezierSkinLocatorName + '.offsetParentMatrix', s=True)[0]
        sourceDecompMtxName = cmds.listConnections(sourceCompMtxName + '.inputQuat', s=True)[0]
        sourceBlendMtxName = cmds.listConnections(sourceDecompMtxName + '.inputMatrix', s=True)[0]
        vectorTailMtxName = cmds.listConnections(sourceBlendMtxName + '.target[0].targetMatrix', s=True)[0]
        vectorHeadMtxName = cmds.listConnections(sourceBlendMtxName + '.inputMatrix', s=True)[0]

        bezierVectorTailDecompMtxName = setDigit('bezierVectorTailDecompMtx')
        bezierVectorTailDecompMtx = cmds.createNode('decomposeMatrix', n=bezierVectorTailDecompMtxName)
        cmds.connectAttr(vectorTailMtxName + '.outputMatrix', bezierVectorTailDecompMtxName + '.inputMatrix')

        bezierVectorHeadDecompMtxName = setDigit('bezierVectorHeadDecompMtx')
        bezierVectorHeadDecompMtx = cmds.createNode('decomposeMatrix', n=bezierVectorHeadDecompMtxName)
        cmds.connectAttr(vectorHeadMtxName + '.outputMatrix', bezierVectorHeadDecompMtxName + '.inputMatrix')

        bezierVectorMinusName = setDigit('bezierVectorMinus')
        bezierVectorMinus = cmds.createNode('plusMinusAverage', n=bezierVectorMinusName)
        cmds.setAttr(bezierVectorMinusName + '.operation', 2)
        cmds.connectAttr(bezierVectorHeadDecompMtxName + '.outputTranslate', bezierVectorMinusName + '.input3D[0]')
        cmds.connectAttr(bezierVectorTailDecompMtxName + '.outputTranslate', bezierVectorMinusName + '.input3D[1]')

        bezierVector4By4MtxName = setDigit('bezierVector4By4Mtx')
        bezierVector4By4Mtx = cmds.createNode('fourByFourMatrix', n=bezierVector4By4MtxName)
        cmds.connectAttr(bezierVectorMinusName + '.output3Dx', bezierVector4By4MtxName + '.in00')
        cmds.connectAttr(bezierVectorMinusName + '.output3Dy', bezierVector4By4MtxName + '.in01')
        cmds.connectAttr(bezierVectorMinusName + '.output3Dz', bezierVector4By4MtxName + '.in02')
        bezier4By4MatrixNames.append(bezierVector4By4MtxName)

        bezierVectorDecompMtxName = setDigit('bezierVectorDecompMtx')
        bezierVectorDecompMtx = cmds.createNode('decomposeMatrix', n=bezierVectorDecompMtxName)
        cmds.connectAttr(bezierVector4By4MtxName + '.output', bezierVectorDecompMtxName + '.inputMatrix')
        cmds.connectAttr(bezierVectorDecompMtxName + '.outputRotate', bezierBlendCompMtxNames[i] + '.inputRotate', f=True)

        i += 1

    return bezier4By4MatrixNames


def setBezierYOrient(bezierBlendCompMtxNames, bezier4By4MatrixNames):
    for i in range(len(bezierBlendCompMtxNames)):
        bezierLastBlendDecompMtxName = cmds.listConnections(bezierBlendCompMtxNames[i] + '.inputTranslate', s=True)[0]
        bezierLastBlendMtxName = cmds.listConnections(bezierLastBlendDecompMtxName + '.inputMatrix', s=True)[0]

        bezierVectorProductName = setDigit('bezierVectorProduct')
        cmds.createNode('vectorProduct', n=bezierVectorProductName)
        cmds.setAttr(bezierVectorProductName + '.operation', 3)
        cmds.setAttr(bezierVectorProductName + '.input1Z', 1)
        cmds.connectAttr(bezierLastBlendMtxName + '.outputMatrix', bezierVectorProductName + '.matrix')
        cmds.connectAttr(bezierVectorProductName + '.outputX', bezier4By4MatrixNames[i] + '.in10')
        cmds.connectAttr(bezierVectorProductName + '.outputY', bezier4By4MatrixNames[i] + '.in11')
        cmds.connectAttr(bezierVectorProductName + '.outputZ', bezier4By4MatrixNames[i] + '.in12')


def progressBar(currentTaskTitle, steps):
    mainProgressBar = mel.eval('$tmp = $gMainProgressBar');

    cmds.progressBar(mainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status=currentTaskTitle, maxValue=steps)

    for i in range(5000):
        if cmds.progressBar(mainProgressBar, query=True, isCancelled=True):
            break

        cmds.progressBar(mainProgressBar, edit=True, step=1)

    cmds.progressBar(mainProgressBar, edit=True, endProgress=True)
