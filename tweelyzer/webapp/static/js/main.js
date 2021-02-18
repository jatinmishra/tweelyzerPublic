$(document).ready(function () {
    // Init
    $('.loader').hide();
    $('#chartContainer').hide();

    // Predict
    $('#predict').click(function () {
        var form_data = new FormData($('#tweet-search')[0]);
        
        if($("#keyword").val().trim() == "") {
           alert("Please Enter a search query.");
           return; 
        }
        

        // Show loading animation
        $(this).hide();
        $('.loader').show();
        $('#chartContainer').hide();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                
                if(data == null || data == "") {
                    alert('No tweets found for the entered search query. Please try again with a different query.');
                } else {
                    counts = data.split(',');
                    neg_count = parseInt(counts[0]);
                    pos_count = parseInt(counts[1]);
                    neu_count = parseInt(counts[2]);
                    total_count = neg_count + pos_count + neu_count;
                    
                    neg_tweet_percent = Math.round((neg_count / total_count) * 100);
                    pos_tweet_percent = Math.round((pos_count / total_count) * 100);
                    neu_tweet_percent = Math.round((neu_count / total_count) * 100);
                    
                    
                    var chart = new CanvasJS.Chart("chartContainer", {
                    	theme: "light2", // "light1", "light2", "dark1", "dark2"
                    	animationEnabled: true,
                    	title: {
                    		text: "Tweet Analysis of top 100 tweets."
                    	},
                    	data: [{
                    		type: "pie",
                    		startAngle: 25,
                    		toolTipContent: "<b>{label}</b>: {y}%",
                    		showInLegend: "true",
                    		legendText: "{label}",
                    		indexLabelFontSize: 16,
                    		indexLabel: "{label} - {y}%",
                    		dataPoints: [
                    			{ y: neg_tweet_percent, label: "Negative Tweets" },
                    			{ y: pos_tweet_percent, label: "Positive Tweets" },
                    			{ y: neu_tweet_percent, label: "Neutral Tweets" }
                    		]
                    	}]
                    });
                    chart.render();                  
                    $('#chartContainer').show();
                }
                $('.loader').hide();
                $('#predict').show();
                console.log('Success!');
            },
        });
    });

});
