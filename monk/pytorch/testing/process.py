from pytorch.testing.imports import *
from system.imports import *

@accepts(str, bool, dict, post_trace=True)
@TraceFunction(trace_args=False, trace_rv=False)
def process_single(img_name, return_raw, system_dict):
    '''
    Run inference on a single image

    Args:
        img_name (str): path to image
        return_raw (bool): If True, then output dictionary contains image probability for every class in the set.
                            Else, only the most probable class score is returned back.
                            

    Returns:
        str: predicted class
        float: prediction score
    '''
    img = Image.open(img_name).convert('RGB');
    img = system_dict["local"]["data_transforms"]["test"](img);
    img = img.unsqueeze(0);
    img = Variable(img);
    img = img.to(system_dict["local"]["device"])
    outputs = system_dict["local"]["model"](img)
    l = outputs.data.cpu().numpy().argmax();
    if(system_dict["dataset"]["params"]["classes"]):
        prediction = system_dict["dataset"]["params"]["classes"][l];
    else:
        prediction = l;
    score = outputs.data.cpu().numpy()[0][l];
    if(return_raw):
        return prediction, score, outputs.data.cpu().numpy()[0];
    else:
        return prediction, score, "";