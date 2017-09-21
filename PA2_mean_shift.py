import cv2
import numpy as np
import time

start_time = time.time()

img = cv2.imread("me.jpg")

rows,cols,depth = img.shape

rgb_array = np.zeros((rows*cols,5))

new_rgb_array = np.zeros((rows,cols,depth))

k=0
# Putting the RGB values into a table
for i in range(0,rows):
	for j in range(0,cols):
			
		rgb_array[k][0],rgb_array[k][1],rgb_array[k][2],rgb_array[k][3],rgb_array[k][4] = img[i][j][0],img[i][j][1],img[i][j][2],i,j

		k=k+1


h_value = 120
iter_value = 30

initial_row_value_for_mean = []
less_than_h = []
total_rows = rows*cols
total_rows = rgb_array.shape[0]
new_mean_value_lesser = []

flag=0

while rgb_array.shape[0] != 0:

	if flag==0:
		index_row = np.random.randint(0,rgb_array.shape[0])
		meanr=rgb_array[index_row][0]
		meang=rgb_array[index_row][1]
		meanb=rgb_array[index_row][2]
		meanx=rgb_array[index_row][3]
		meany=rgb_array[index_row][4]

	index = []
	for i in range(0,rgb_array.shape[0]):
		euclid_dist = ((rgb_array[i][0]-meanr)**2 + (rgb_array[i][1]-meang)**2 + (rgb_array[i][2]-meanb)**2 + (rgb_array[i][3]-meanx)**2 + (rgb_array[i][4]-meany)**2)**0.5
		if euclid_dist <= h_value:
			less_than_h.append(rgb_array[i])
			index.append(i)


	if len(less_than_h) >0:
		mean_for_first_element,mean_for_second_element,mean_for_third_element,mean_for_fourth_element,mean_for_fifth_element = 0,0,0,0,0

		for i in range(0,len(less_than_h)):
			mean_for_first_element = mean_for_first_element + less_than_h[i][0]
			mean_for_second_element = mean_for_second_element + less_than_h[i][1]
			mean_for_third_element = mean_for_third_element + less_than_h[i][2]
			mean_for_fourth_element = mean_for_fourth_element + less_than_h[i][3]
			mean_for_fifth_element = mean_for_fifth_element + less_than_h[i][4]

		mean_for_first_element,mean_for_second_element,mean_for_third_element,mean_for_fourth_element,mean_for_fifth_element = mean_for_first_element/len(less_than_h),mean_for_second_element/len(less_than_h),mean_for_third_element/len(less_than_h),mean_for_fourth_element/len(less_than_h),mean_for_fifth_element/len(less_than_h)

		new_mean_value_lesser = [mean_for_first_element,mean_for_second_element,mean_for_third_element,mean_for_fourth_element,mean_for_fifth_element]

		new_euclid_dist = ((mean_for_first_element-meanr)**2 + (mean_for_second_element-meang)**2 + (mean_for_third_element-meanb)**2 + (mean_for_fourth_element-meanx)**2 + (mean_for_fifth_element-meany)**2)**0.5


		if new_euclid_dist <= iter_value:
			for i in range(0,len(index)):
				row = int((less_than_h[i])[3])
				col = int((less_than_h[i])[4])
				new_rgb_array[row][col][0] = mean_for_first_element
				new_rgb_array[row][col][1] = mean_for_second_element
				new_rgb_array[row][col][2] = mean_for_third_element

			rgb_array = np.delete(rgb_array,index,0)
			flag=0
		else:
			meanr=mean_for_first_element
			meang=mean_for_second_element
			meanb=mean_for_third_element
			meanx=mean_for_fourth_element
			meany=mean_for_fifth_element
			flag=1
		print ("length ",rgb_array.shape[0])

	less_than_h = []

print new_rgb_array

cv2.imwrite("me_segmented.jpg", new_rgb_array)
cv2.waitKey(0)

execution_time = (time.time() - start_time)
print 'Execution finished in ' + str(round(execution_time, 2)) + 'secs'

