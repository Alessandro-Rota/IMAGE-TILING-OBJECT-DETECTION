def to_yolo(path):
    '''
    This function converts 
    annotatiions to YOLO format 
    '''
    for image in os.listdir(path):
        if image.endswith(".png"):
            im = cv2.imread(path + image)
            h, w, _ = im.shape
            annot_name = image.replace(image.split(".")[-1], "txt")
            if os.path.exists(path + annot_name):
                annotations = pd.read_csv(path + annot_name, sep = " ", names = ["xc", "yc", "angle", "class", "isEntire", "occluded", "x1", "x2", "x3", "x4", "y1", "y2", "y3", "y4"])
                annotations.drop(columns = ["xc", "yc", "angle", "isEntire", "occluded"], inplace = True)
                annotations["class"].replace(31, 3, inplace = True)
                annotations["class"].replace(23, 6, inplace = True)
                annotations["class"].replace(11, 7, inplace = True)
                annotations["class"].replace(10, 8, inplace = True)
                annotations["class"] = annotations["class"] - 1
                annotations["xmin"] = annotations[["x1", "x2", "x3", "x4"]].min(axis = 1)
                annotations["xmax"] = annotations[["x1", "x2", "x3", "x4"]].max(axis = 1)
                annotations["ymin"] = annotations[["y1", "y2", "y3", "y4"]].min(axis = 1)
                annotations["ymax"] = annotations[["y1", "y2", "y3", "y4"]].max(axis = 1)
                annotations.drop(columns = ["x1", "x2", "x3", "x4", "y1", "y2", "y3", "y4"], inplace = True)
                annotations["xc"] = (annotations["xmin"] + annotations["xmax"])/2/w
                annotations["yc"] = (annotations["ymin"] + annotations["ymax"])/2/h
                annotations["w"] = (annotations["xmax"] - annotations["xmin"])/w
                annotations["h"] = (annotations["ymax"] - annotations["ymin"])/h
                annotations.drop(columns = ["xmin", "xmax", "ymin", "ymax"], inplace = True)
                annotations.to_csv(path + annot_name, sep = " ", index = False, header = False, float_format = "%.6f")    
            else:
                print("annotations not available for", annot_path + annot_name )
    
    