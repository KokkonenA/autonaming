#!/usr/bin/env python

import DaVinciResolveScript as dvr

resolve = dvr.scriptapp('Resolve')

projectManager = resolve.GetProjectManager()

mediaPool = projectManager.GetCurrentProject().GetMediaPool()

clips = mediaPool.GetRootFolder().GetClips()

videoFiles = []
audioFiles = []

# separate video and audio files to their own lists
for clipIdx in clips:
	clip = clips[clipIdx]
	type = clip.GetClipProperty()['Type']
	
	if 'Video' in type:
		videoFiles.append(clip)
	elif 'Audio' in type:
		audioFiles.append(clip)

# add take numbers to metadata

scene = '0'
take = 1

for file in videoFiles:
	newScene = file.GetMetadata('Scene')
	
	if (newScene == scene):
		take += 1
	else:
		scene = newScene
		take = 1

	file.SetMetadata('Take', str(take))


def hasAudio(videoFile):
	comments = videoFile.GetMetadata('Comments')
	return (len(comments) == 0 or 'MOS' not in comments['Comments'])

videoFilesFiltered = filter(hasAudio, videoFiles)

def fileName(file):
	return file.GetClipProperty()['File Name']

videoFilesFiltered.sort(key = fileName)
audioFiles.sort(key = fileName)

for i in range(0, len(videoFilesFiltered) - 1):
	metadata = videoFilesFiltered[i].GetMetadata()
	audioFile = audioFiles[i]

	audioFile.SetMetadata('Scene', metadata['Scene'] )
	audioFile.SetMetadata('Take', metadata['Take'])