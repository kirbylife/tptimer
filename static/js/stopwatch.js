/*      https://gist.github.com/electricg/4372563
Copyright (c) 2010-2015 Giulia Alfonsi <electric.g@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/
var	clsStopwatch = function() {
		// Private vars
		var	startAt	= 0;	// Time of last start / resume. (0 if not running)
		var	lapTime	= 0;	// Time on the clock when last stopped in milliseconds

		var	now	= function() {
				return (new Date()).getTime();
			};

		// Public methods
		// Start or resume
		this.start = function() {
				startAt	= startAt ? startAt : now();
			};

		// Stop or pause
		this.stop = function() {
				// If running, update elapsed time otherwise keep it
				lapTime	= startAt ? lapTime + now() - startAt : lapTime;
				startAt	= 0; // Paused
			};

		// Reset
		this.reset = function() {
				lapTime = startAt = 0;
			};

		// Duration
		this.time = function() {
				return lapTime + (startAt ? now() - startAt : 0);
			};
	};

console.log("Si entro");
var x = new clsStopwatch();
var $time;
var times={
    "2x2x2":[],
    "3x3x3":[],
    "4x4x4":[],
    "5x5x5":[],
    "6x6x6":[],
    "7x7x7":[],
    "piraminx":[],
    "skewb":[],
    "clock":[],
    "megaminx":[],
    "squareone":[]
};
var $lista;
var $cube;
var $scramble;

var $media;
var $desviacion;
var $mejor;
var $peor;

var clocktimer;

function pad(num, size) {
	var s = "0000" + num;
	return s.substr(s.length - size);
}

function formatTime(time) {
	var h = m = s = ms = 0;
	var newTime = '';

	h = Math.floor( time / (60 * 60 * 1000) );
	time = time % (60 * 60 * 1000);
	m = Math.floor( time / (60 * 1000) );
	time = time % (60 * 1000);
	s = Math.floor( time / 1000 );
	ms = time % 1000;

	newTime = pad(h, 2) + ':' + pad(m, 2) + ':' + pad(s, 2) + ':' + pad(ms, 3);
	//newTime = newTime.substr(0,newTime.length-1);
	return newTime;
}

function show() {
	$time = document.getElementById('time');
	$lista = document.getElementById('total');
	$cube = document.getElementById('cube');
	$scramble = document.getElementById('scramble');

	$media = document.getElementById('media');
	$desviacion = document.getElementById('desviacion');
	$mejor = document.getElementById('mejor');
	$peor = document.getElementById('peor');

	setScramble();
	update();
}

function update() {
	$time.innerHTML = formatTime(x.time());
}

function start() {
	clocktimer = setInterval("update()", 1);
	x.start();
}

function stop() {
	x.stop();
	if(x.time()!=0){
	    //$lista.innerHTML="<li>"+$time.innerHTML+" -> "+$scramble.innerHTML+"</li>"+$lista.innerHTML;
	    $.ajax({
	        data:{
	            "cube":$("#cube").val(),
	            "time":x.time(),
	            "displayTime":time.innerHTML,
	            "scramble":$scramble.innerHTML
            },
	        url:"/setTime",
            //url:"/generateScramble/"+$("#cube").val(),
            success:function(result){
                console.log(result);
            }
        });
	    times[$("#cube").val()].push([x.time(),$scramble.innerHTML,$time.innerHTML]);
	    setTimes();
	    setScramble();
	}
	clearInterval(clocktimer);
}

function reset() {
	//stop();
	x.reset();
	update();
}

function setTimes(){
    var str="";
    if(times[$("#cube").val()].length>0){
        var val;
        var med=0;
        var desv=0;
        var max=times[$("#cube").val()][0][0];
        var min=times[$("#cube").val()][0][0];
        for(var c=0;c<times[$("#cube").val()].length;c++){
            val=times[$("#cube").val()][c][0];
            med=med+val;
            if(val>max){
                max=val;
            }
            if(val<min){
                min=val;
            }
        }
        for(var c=0;c<times[$("#cube").val()].length;c++){
            val=times[$("#cube").val()][c][0];
            scram=times[$("#cube").val()][c][1];
            tiem=times[$("#cube").val()][c][2];
            if(val==min){        //Verde - Mejor tiempo
                str="<tr><td style='background-color:#64FF62'>"+tiem+"</td><td>"+scram+"</td><td><div class='btn-group '><button class='btn btn-sm btn-warning'>+2</button><button class='btn btn-sm btn-danger'>DNF</button><button class='btn btn-sm btn-outline-danger' onclick='removeTime("+c+")'><i class='fa fa-times' aria-hidden='true'></i></div></button></td></tr>"+str;
            }
            else if(val==max){  //Rojo - Peor tiempo
                str="<tr><td style='background-color:#FF6962'>"+tiem+"</td><td>"+scram+"</td><td><button class='btn btn-sm btn-warning'>+2</button><button class='btn btn-sm btn-danger'>DNF</button><button class='btn btn-sm btn-outline-danger' onclick='removeTime("+c+")'><i class='fa fa-times' aria-hidden='true'></i></button></td></tr>"+str;
            }
            else{               //Nada - Tiempo meh
                str="<tr><td>"+tiem+"</td><td>"+scram+"</td><td><button class='btn btn-sm btn-warning'>+2</button><button class='btn btn-sm btn-danger'>DNF</button><button class='btn btn-sm btn-outline-danger' onclick='removeTime("+c+")'><i class='fa fa-times' aria-hidden='true'></i></button></td></tr>"+str;
            }
        }
        if(times[$("#cube").val()].length>1){
            med=med/times[$("#cube").val()].length;
            for(var c=0;c<times[$("#cube").val()].length;c++){
                val=times[$("#cube").val()][c][0];
                desv=desv+Math.pow(val-med,2);
            }
            desv=desv/times[$("#cube").val()].length-1;
            desv=Math.pow(desv,0.5);
            $desviacion.innerHTML=formatTime(Math.round(desv));
        }
        $media.innerHTML=formatTime(Math.round(med));
        $mejor.innerHTML=formatTime(min);
        $peor.innerHTML=formatTime(max);
        $lista.innerHTML="<table style='width:100%'><th>Tiempo</th><th>Scramble</th>"+str+"</table>";
    }
    else{
        $desviacion.innerHTML=$media.innerHTML=$mejor.innerHTML=$peor.innerHTML="0:00";
        $lista.innerHTML="<table><th>Tiempo</th><th>Scramble</th></table>";
    }
}

function removeTime(num){
    times[$("#cube").val()].splice(num,1);
    setTimes();
}

function setScramble(){
    setTimes();
     document.getElementById("cube").blur();
    $.ajax({
        url:"/generateScramble/"+$("#cube").val(),
        success:function(result){
            $scramble.innerHTML=result;
        }
    });
}