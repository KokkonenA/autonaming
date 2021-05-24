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

# sort files by date of creation
def fileDate(file):
	return file.GetClipProperty()['Date Created']

videoFiles.sort(key = fileDate)
audioFiles.sort(key = fileDate)

# add take numbers to metadata
scene = '0'
take = 1

for file in videoFiles:
	newScene = file.GetMetadata()['Scene']
	
	if (newScene == scene):
		take += 1
	else:
		scene = newScene
		take = 1

	file.SetMetadata('Take', str(take))

# returns true if no 'MOS' found in comments (audio was recorded to a separate file at the same time)
def hasAudio(videoFile):
	comments = videoFile.GetMetadata('Comments')
	return (len(comments) == 0 or 'MOS' not in comments['Comments'])

# filter only the takes for wich also audio was recorded
videoFilesFiltered = filter(hasAudio, videoFiles)

for i in range(0, len(videoFilesFiltered)):
	metadata = videoFilesFiltered[i].GetMetadata()
	audioFile = audioFiles[i]

	audioFile.SetMetadata('Scene', metadata['Scene'] )
	audioFile.SetMetadata('Take', metadata['Take'])

	print('Done!')