<?php
function isFileExistFirstLine($file){
	if(!feof($file)){
		$line = fgets($file);
		if(strlen($line) > 0){
			return true;
		}
	}
	return false;
}

function writeCommonLog($data){
	$filePath = sprintf('./common_%s.log', date('Y-m-d'));
	$logFile = fopen($filePath, 'a') or die("Unable to open file!");
	fwrite($logFile, $data);
	fclose($logFile);	
}

function writeOneLog($data){
	$tmpArr = explode("|",$data);
	$arrLength=count($tmpArr);
	if ($arrLength > 0) {
		if($arrLength == 4){
			$userAgent = $tmpArr[0];
			$filePath = sprintf('./%s_%s.log', md5($userAgent), date('Y-m-d'));
			$time = date('Y-m-d H:i:s', (int)$tmpArr[1]);
			$logFile = fopen($filePath, "a+") or die("Unable to open file!");
			$output = sprintf("[%s] %s : %s\n", $tmpArr[2], $time, $tmpArr[3]);
			if(!isFileExistFirstLine($logFile)){
				fwrite($logFile, "{$userAgent}\n\n");
			}
			fwrite($logFile, $output);
			fclose($logFile);
		}else{
			writeCommonLog($data);
		}
	}
}

function getOneLogInfo($data){
	$tmpArr = explode("|",$data);
	$arrLength=count($tmpArr);
	if ($arrLength > 0) {
		$info = array();
		if($arrLength == 4){
			$userAgent = $tmpArr[0];
			$filePath = sprintf('./%s_%s.log', md5($userAgent), date('Y-m-d'));
			$time = date('Y-m-d H:i:s', (int)$tmpArr[1]);
			$output = sprintf("[%s] %s : %s\n", $tmpArr[2], $time, $tmpArr[3]);
			$info['header'] = $userAgent;		
			$info['filePath'] = $filePath;
			$info['output'] = $output;			
		}else{
			$info['filePath'] = sprintf('./common_%s.log', date('Y-m-d'));
			$info['output'] = $data;
		}
		return $info;
	}
	return null;
}

			// $logFile = fopen($filePath, "a+") or die("Unable to open file!");
function parseOneFormData($data){
	$ret = array();
	$dataArr = explode("\r\n", $data);
	$ret['disposition'] = $dataArr[0];
	$ret['type'] = $dataArr[1];	
	$ret['body'] = $dataArr[3];
	return $ret;
}

function parseAllFormData($data){
	$retArr = array();
	$tmpArr = preg_split("/------WebKitFormBoundary[a-zA-Z0-9\-]+\r\n/", $data, -1, PREG_SPLIT_OFFSET_CAPTURE);
	foreach($tmpArr as $one){
		$str=$one[0];
		if(strlen($str) > 0){
			$logObj = parseOneFormData($str);
			array_push($retArr, $logObj); 
		}
	}
	return $retArr;
}

function parseAllLogData($mutilData){
	$dataArr = explode("\n",$mutilData);
	// writeCommonLog($mutilData."\n");
	$logArr = array();
	$fileArr = array();
	foreach($dataArr as $data){
		if(strlen($data) > 0){	
			$info = getOneLogInfo($data);
			if(!is_null($info)){
				// array_push($logArr, $info);
				$filePath = $info['filePath'];
				if(!array_key_exists($filePath, $info)){
					$fileArr[$filePath] = fopen($filePath, "a+");
				}
				$logFile = $fileArr[$filePath];
				if(!isFileExistFirstLine($logFile)){
					if(array_key_exists('header', $info)){
						fwrite($logFile, $info['header']);
						fwrite($logFile, "\n\n");
					}
				}
				fwrite($logFile, $info['output']);
				fwrite($logFile, "\n");
			}
		}
	}
	foreach($fileArr as $name=>$file){
		fclose($file);
	}
}

function isWebKitFormBoundary($data){
	$headStr = '------WebKitFormBoundary';
	$tmpStr = substr($data,0,strlen($headStr));
	return strcmp($headStr, $tmpStr) == 0;
}

//$data=userAgent|time|type|msg
$mutilData = file_get_contents('php://input', 'r');
if($mutilData){
	if(isWebKitFormBoundary($mutilData)){
		$formObjArray = parseAllFormData($mutilData);
		// writeCommonLog(json_encode($formObjArray)."\n");
		if(count($formObjArray) > 0){
			foreach($formObjArray as $formObj){
				parseAllLogData($formObj['body']);
			}
		}
	}else{
		parseAllLogData($mutilData);
	}
}
?>