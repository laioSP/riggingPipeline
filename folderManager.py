import os
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

class projectManager:
    def __init__(self):
        self.user = os.getlogin()
        self.mainPath = os.path.join('/home', self.user, 'shows')
        self.show = 'no show'
        self.asset = 'no asset'
        self.version = 'no versions'
        self.mayaFile = 'no maya file'
        self.showPath = 'no show path'
        self.assetPath = 'no asset path'
        self.versionPath = 'no version path'
        self.mayaFilePath = 'no maya file path'

    def getProjectFolder(self): 
        return pm.workspace(query=True, rootDirectory=True)

    def getShowList(self):
        showList = os.listdir(self.mainPath)
        showList.sort()
        return showList
        
    def getAssetList(self, show):
        self.show = show
        self.showPath = os.path.join(self.mainPath, self.show)
        assetList = os.listdir(self.showPath)
        assetList.sort()
        return assetList

    def getVersionList(self, asset):
        self.asset =  asset
        self.assetPath  = os.path.join(self.showPath, self.asset)
        fileList = os.listdir(self.assetPath)
        
        versionFolders = []
        for v in fileList:
            if v[0] == 'V':
                if len(v) == 5:
                    versionFolders.append(v)

        if versionFolders:
            versionFolders.sort()
            self.version = versionFolders[-1]
            self.versionPath = os.path.join(self.assetPath, self.version)
            return versionFolders
        else :
            self.version = 'no version'
            
        return [self.version]
        
    def createNewVersion(self):
        versionList = self.getVersionList(self.asset)

        if self.version == 'no version':    
            self.version = 'V{:04d}'.format(1)

        else:
            self.version = 'V{:04d}'.format(len(versionList) +1)

        self.versionPath = os.path.join(self.assetPath, self.version)

        return os.mkdir(self.versionPath)    

    def setProject(self):

        mayaFiles = self.getMayaFiles()
        if self.mayaFile == 'no maya file':

            self.mayaFile = '{}_0001.ma'.format(self.asset)
            self.mayaFilePath = os.path.join(self.versionPath, self.mayaFile)
            cmds.file( f=True, new=True )    
            cmds.file( rename= self.mayaFile )
            cmds.file( save=True, type='mayaAscii' )

        else:
            self.mayaFile = '{}_{:04d}.ma'.format(self.asset, len(mayaFiles))
            #mel.eval('setProject "{}"'.format(self.mayaFilePath))
            cmds.file( self.mayaFilePath, o=True )

    def getMayaFiles(self):
        fileList = os.listdir(self.versionPath)
        mayaFiles = []
        for file in fileList:
            if file.endswith('.ma'):
                mayaFiles.append(file)

        if mayaFiles:
            mayaFiles.sort()
            self.mayaFile = mayaFiles[-1]
            self.mayaFilePath = os.path.join(self.versionPath, self.mayaFile)
        return mayaFiles
    
    def loadAsset(self):
        print(self.show)
        print(self.versionPath )
        if self.version == 'no versions':
            self.createNewVersion()
        self.setProject()
        #self.save()

    def save(self):
        mayaFiles = self.getMayaFiles()

        if mayaFiles:
            counter = len(mayaFiles) + 1
        else:
            counter = 1

        cmds.file( rename='{}Rig_{:04d}.ma'.format(self.asset, counter) )
        file = cmds.file( save=True, type='mayaAscii' )
        return file

    def publish(self):
        self.createNewVersion(self.version + 1)
        self.setProject()
        self.save()


















