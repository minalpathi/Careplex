$(document).ready(function(){

    // $("#doctor-page").hide();
    // $("#revenue-page").hide();

    //function to toggle left menu
    $('#menu_toggle').on('click',function(){
        $('.left_col').toggle();
        $('.right_col').toggleClass("full-dashboard");
        $('.main_container .top_nav').toggleClass("full-dashboard");
    });

    $('.close-link').on('click',function(event){
        console.log(event);
    });

    //function to load doctor page
    $('#doctor').on('click',function(){
        $('#landing-page').hide();
        $("#revenue-page").hide();
        $("#doctor-page").load('/doctor');
        $("#doctor-page").show();

    });
    
    $('#revenue').on('click',function(){
        $('#landing-page').hide();
        $("#doctor-page").hide();
        $("#revenue-page").load('/revenue');
        $("#revenue-page").show();

    });

});


