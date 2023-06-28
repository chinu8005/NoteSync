gsap.registerPlugin(ScrollTrigger);
gsap
  .timeline({
    scrollTrigger: {
      trigger: ".image-board",
      pin: true,
      start: "top top",
      end: "+=300%",
      scrub: 1,
    },
    defaults: {
      ease: "none",
    },
  })
  .to(
    document.body, {
      delay: 0.3,
      backgroundColor: "transperent",
    },
    "start"
  )
  .to(
    ".main-text",
    { 
      x: -1000,
      zIndex: 10,
    },
    "start"
  )
  .to(
    ".main-discription",
    {
      x: 1000,
    },
    "start"
  )
  .to(
    ".main-discription",
    {
      opacity:0,
    },
    "start"
  )
  .to(
    ".btn-white",
    {
      delay: 0.1,
      x: 1000,
    },"start"
   )
    .to(
    "#main-image",
    {
        delay: 0.1,
        opacity: 0,
    },
    "start"
    )
    .to(
    ".first-section",
    {
        opacity: 0,
    },
    "start"
    ).to(
    ".ud-section",
    {   delay: 0.3,
        opacity: 10,
    },
    "start"
    )
    .to(
    ".ud-scale-img",
    {
        delay: 0.4,
        y: -1000,
    },
    "start"
    )
    .to(
    ".ud-title",
    {   delay: 0.4,
        y: -100,
    },
    
    "start"
    )
    .to(
    ".ud-sub-text",
    {   delay: 0.4,
        y: 100,
    },
    
    "start"
    )
    .to(
    ".ud-btn",
    {   delay: 0.4,
        y: 100,
    },
    
    "start"
    ).to(
      ".ud-title",
      {   
        delay: 0.3,
        opacity:0,
      },
      
      "start"
      )
      .to(
      ".ud-sub-text",
      { 
        delay: 0.3,  
        opacity:0,
      },
      
      "start"
      )
      .to(
      ".ud-btn",
      {   
        delay: 0.3,
        opacity:0,
      },
      
      "start"
      ).to(
      ".ud-section",
      {   delay: 0.5,
          opacity: 0,
      },
      
      "start"
    ).to(
    ".leaderboard-sect",
      { delay: 0.7,
        opacity: 10,
      },
      
      "start"
      )  
    .to(
      ".lead-maintxt",
      {   delay: 0.8,
          x: -2500,
      },
      
      "start"
    )
    .to(
      ".lead-subtxt",
      {   delay: 0.8,
          y: 2000,
      },
      
      "start"
    )
    .to(
      ".card-r1",
      {
          delay: 0.8,
          x: 4000,
      },
      
      "start"
    )
    .to(
      ".card-r2",
      {
          delay: 0.8,
          x: -4000,
      },
      
      "start"
    )
    .to(
      ".card-r3",
      {
          delay: 0.8,
          x: 4000,
      },
      
      "start"
    )
    .to(
      ".card-r4",
      {
          delay: 0.8,
          x: 4000,
      },
      
      "start"
    )
    .to(
      ".lead-line",
      {
          delay: 0.8,
          scale: 10,
      },
      
      "start"
    )
    .to(
      ".lead-line",
      {
          delay: 0.8,
          opacity: 0,
      },
      
      "start"
    )
    .to(
    ".leaderboard-sect",
    {
        delay: 0.9,
        opacity: 0,
    },
    
    "start"
    )
    .to(
    ".reward-sect",
    {
        delay: 0.9,
        opacity: 15,
    },
    "start"
    );
  